import board
import digitalio
import busio
import time

import st7735r
import gamepad
import neopixel_write


K_X = 0x01
K_DOWN = 0x02
K_LEFT = 0x04
K_RIGHT = 0x08
K_UP = 0x10
K_O = 0x20


dc = digitalio.DigitalInOut(board.MISO)
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
spi.try_lock()
spi.configure(baudrate=100000, polarity=0, phase=0)
time.sleep(0.2)
display = st7735r.ST7735R(spi, dc, 0b110)
spi.configure(baudrate=23000000, polarity=0, phase=0)
buttons = gamepad.GamePad(
    digitalio.DigitalInOut(board.D5),
    digitalio.DigitalInOut(board.D11),
    digitalio.DigitalInOut(board.D12),
    digitalio.DigitalInOut(board.D9),
    digitalio.DigitalInOut(board.D10),
    digitalio.DigitalInOut(board.D6),
)
try:
    pin = digitalio.DigitalInOut(board.NEOPIXEL)
    pin.switch_to_output()
    neopixel_write.neopixel_write(pin, b'\x00\x00\x00')
except Exception:
    pass
