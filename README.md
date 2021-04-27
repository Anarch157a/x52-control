import usb.core
from gx52.driver.x52_driver import X52Driver, X52ColoredLedStatus, X52LedStatus, X52DateFormat, X52MfdLine, X52DeviceType, X52Device

usb=usb.core.find(idVendor=0x06a3, idProduct=0x0762)

dev=X52Device(0x06a3, 0x0762, X52DeviceType.X52_PRO, 'hot.as')

joy=X52Driver(usb,dev)

joy.set_mfd_text(X52MfdLine.LINE1,'xupacabra')

## commands

ID_VENDOR = 0x06a3
ID_PRODUCTS = [0x0762, 0x0255, 0x075c]

### X52 vendor API commands

- Vendor request - all commands must have this request ID

_X52_VENDOR_REQUEST = 0x91

- MFD Text commands

-X52_MFD_CLEAR_LINE = 0x08

- Brightness commands

MFD_BRIGHTNESS = 0xb1
LED_BRIGHTNESS = 0xb2

X52_BRIGHTNESS_MIN = 0x00
X52_BRIGHTNESS_MAX = 0x80 / 4

- LED set commands

_X52_LED = 0xb8

- Time commands

TIME_CLOCK1 = 0xc0
OFFS_CLOCK2 = 0xc1
OFFS_CLOCK3 = 0xc2

- Date commands

DDMM = 0xc4
YEAR = 0xc8

- Date Format

YYMMDD = 0
DDMMYY = 1
MMDDYY = 2

- Shift indicator on MFD

_X52_SHIFT_INDICATOR = 0xfd

- Shift Status

ON = 0x51
OFF = 0x50

- Blink throttle & POV LED

_X52_BLINK_INDICATOR = 0xb4

- Blink Status

ON = 0x51
OFF = 0x50

_X52_MFD_LINE_SIZE = 16

- Flag bits

_X52_FLAG_IS_PRO = 0

- Indicator bits for update mask

_X52_BIT_SHIFT = 0

- Mfd Line

LINE1 = 0xd1
LINE2 = 0xd2
LINE3 = 0xd4

_WRITE_TIMEOUT = 5000

X52 Device Type

X52_PRO = 'X52 Pro'
X52 = 'X52'

---------

X52Led(IntEnum):
    X52_BIT_LED_FIRE = 1
    X52_BIT_LED_THROTTLE = 20

X52LedRed(IntEnum):
    X52_BIT_LED_A_RED = 2
    X52_BIT_LED_B_RED = 4
    X52_BIT_LED_D_RED = 6
    X52_BIT_LED_E_RED = 8
    X52_BIT_LED_T1_RED = 10
    X52_BIT_LED_T2_RED = 12
    X52_BIT_LED_T3_RED = 14
    X52_BIT_LED_POV_RED = 16
    X52_BIT_LED_I_RED = 18

X52LedGreen(IntEnum):
    X52_BIT_LED_A_GREEN = 3
    X52_BIT_LED_B_GREEN = 5
    X52_BIT_LED_D_GREEN = 7
    X52_BIT_LED_E_GREEN = 9
    X52_BIT_LED_T1_GREEN = 11
    X52_BIT_LED_T2_GREEN = 13
    X52_BIT_LED_T3_GREEN = 15
    X52_BIT_LED_POV_GREEN = 17
    X52_BIT_LED_I_GREEN = 19

X52LedStatus(IntEnum):
    OFF = 0
    ON = 1

X52ColoredLedStatus(IntEnum):
    OFF = 0
    GREEN = 1
    RED = 2
    AMBER = 3


=============

BOTAO A:

191     def set_led_a(self, led: X52ColoredLedStatus) -> None:⏎
192         self._set_colored_led_status(led, X52LedRed.X52_BIT_LED_A_RED, X52LedGreen.X52_BIT_LED_A_GREEN)⏎


( __LED_STATUS 

291     def _set_colored_led_status(self, led_status: X52ColoredLedStatus, red: X52LedRed, green: X52LedGreen) -> None:⏎
292         if led_status == X52ColoredLedStatus.RED:⏎
293             self._set_led_status(green.value, X52LedStatus.OFF)⏎
294             self._set_led_status(red.value, X52LedStatus.ON)⏎
295         elif led_status == X52ColoredLedStatus.GREEN:⏎
296             self._set_led_status(green.value, X52LedStatus.ON)⏎
297             self._set_led_status(red.value, X52LedStatus.OFF)⏎
298         elif led_status == X52ColoredLedStatus.AMBER:⏎
299             self._set_led_status(green.value, X52LedStatus.ON)⏎
300             self._set_led_status(red.value, X52LedStatus.ON)⏎
301         elif led_status == X52ColoredLedStatus.OFF:⏎
302             self._set_led_status(green.value, X52LedStatus.OFF)⏎
303             self._set_led_status(red.value, X52LedStatus.OFF)⏎
304         else:⏎
305             raise ValueError(f"Unsupported ColoredLedStatus: ${led_status.name}")⏎


286     def _set_led_status(self, led, status):⏎
287         value = led << 8⏎
288         value += led_status.value⏎
289         self._vendor_command(_X52_LED, value)⏎


chama __set_led_status passando __LED_CODE (1 a 20) e __LED_STATUS ( 0 ou 1 ) 

valor do comando= ( __LED_CODE << 8 ) + status : repetir p/ red e green se aplicavel

value: valor do comando
vendor_command: comando a executar

- LED set commands (vendor_command)
_X52_LED = 0xb8 ()

return self.usb_device.ctrl_transfer(64, _X52_VENDOR_REQUEST, value, vendor_command, None, _WRITE_TIMEOUT)
_X52_VENDOR_REQUEST = 0x91

