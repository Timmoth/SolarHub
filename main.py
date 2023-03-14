import time
import board
import digitalio
import busio
import INA219

i2c = busio.I2C(board.GP5, board.GP4)
sensor = INA219.INA219(i2c)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)
    print("Voltage:   {} V".format(sensor.bus_voltage))
    print("Current:       {} mA".format(sensor.current))
    print("Power: {} W".format(sensor.power))
