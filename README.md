# Logitech X52/X52Pro module

Most of the information about how to configure the devices comes from a GUI program called gx52, created by Roberto Leinardi. His project can be found at https://github.com/leinardi/gx52 . Many thanks to him for his efforts, if you need a GUI app to set up your HOTAS, consider using his program.

As I develop this module more, I'll be adding more documentation.

Right now, only setting LED colors and blinking status are implemented.

-----------

## How to use it

- Initializing the module

```python
from x52 import x52

# locate all devices
joystick = x52()

# list devices
print(joystick.devices)
```

- Setting button colors

```python
# sets POV LED to green on device 0
joystick.set_led_color(joystick.devices[0], 'pov', 'green')

# Blinks I button and POV Hat 1
joystick.set_led_blink(joystick.devices[0], 'blink')

# stops blinking
joystick.set_led_blink(joystick.devices[0], 'solid')
```

Valid colors for POV Hat 2 and Throtlle are `on` and `off`. For all other buttons values are `amber`, `red`, `green` or `off`.

For blinking status, values are `blink` and `solid`.
