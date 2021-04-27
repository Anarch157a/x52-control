#!/usr/bin/env pthon3

import datetime
import usb.util
from usb.core import Device

class Invalid_Setting(Exception):
    def __init__(self, message):
        self.message = message

class x52:

    __VENDOR_ID=0x06a3
    __SUPPORTED_DEVICES = (
        { 'product_id': 0x0762, 'device_type': 'X52 Pro', 'model': 'Saitek PLC Saitek X52 Pro Flight Control System'},
        { 'product_id': 0x0255, 'device_type': 'X52', 'model': 'Saitek PLC X52 Flight Controller'},
        { 'product_id': 0x075c, 'device_type': 'X52', 'model': 'Saitek PLC X52 Flight Controller'}
        )
    
    __LED_STATUS = {
        'off': 0,
        'on':  1,
        'blink': 0x51,
        'solid': 0x50
        }

    __WRITE_TIMEOUT = 5000

    __LED_CODE = {
        'fire':      { 'red': None, 'green':  1 },
        'a':         { 'red':  2,   'green':  3 },
        'b':         { 'red':  4,   'green':  5 },
        'd':         { 'red':  6,   'green':  7 },
        'e':         { 'red':  8,   'green':  9 },
        't1':        { 'red': 10,   'green': 11 },
        't2':        { 'red': 12,   'green': 13 },
        't3':        { 'red': 14,   'green': 15 },
        'pov':       { 'red': 16,   'green': 17 },
        'i':         { 'red': 18,   'green': 19 },
        'throttle':  { 'red': None, 'green': 20 }
        }

    # Vendor requesto code for the ctrl_transfer function
    __VENDOR_REQUEST = 0x91
    # LED set commands
    __VENDOR_COMMAND = { 'led': 0xb8, 'blink': 0xb4 }

    devices = []

    def __init__(self):
        for devs in self.__SUPPORTED_DEVICES:
            self.devices += list(usb.core.find(
                idVendor=self.__VENDOR_ID,
                idProduct=devs['product_id'],
                find_all=True))

    def __send_command__(self, device: Device, vendor_command: int, value: int):
        return device.ctrl_transfer(64, self.__VENDOR_REQUEST, value, vendor_command, None, self.__WRITE_TIMEOUT)

    def set_led_color(self, device: Device, led: str, color: str):
        """
        Sets the LED color for different buttons on the joystick.
        For the throtlle and Fire button, the valid values are 'on' or 'off'.
        For buttons A, B, D, E, I, T1, T2, T3 and POV Hat, the valid values
        are 'amber', 'red', 'green' and 'off'.
        """
        color_combos = {
            'amber': { 'red': self.__LED_STATUS['on'],  'green': self.__LED_STATUS['on'] },
            'green': { 'red': self.__LED_STATUS['off'], 'green': self.__LED_STATUS['on'] },
            'red':   { 'red': self.__LED_STATUS['on'],  'green': self.__LED_STATUS['off'] },
            'on':    { 'red': self.__LED_STATUS['off'], 'green': self.__LED_STATUS['on'] },
            'off':   { 'red': self.__LED_STATUS['off'],  'green': self.__LED_STATUS['off'] }
            }
        if color not in [ 'amber', 'red', 'green', 'on', 'off']:
            raise Invalid_Setting(f'Color "{color}" is invalid')
        if led in [ 'throttle', 'fire' ] and color not in [ 'on', 'off' ]:
            raise Invalid_Setting(f'Color "{color}" is invalid for "{led}"')
        for col,code in color_combos[color].items():
            if self.__LED_CODE[led][col]:
                self.__send_command__(device, self.__VENDOR_COMMAND['led'], ( self.__LED_CODE[led][col] << 8 ) + code )

    def set_led_blink(self, device: Device, state: str):
        if state not in [ 'blink', 'solid' ]:
            raise Invalid_Setting(f'Invalid  setting {state}')
        self.__send_command__(device, self.__VENDOR_COMMAND['blink'], self.__LED_STATUS[state] )
