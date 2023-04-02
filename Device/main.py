import time
import board
import digitalio
import busio
import INA219
import os
import wifi
import socketpool
import adafruit_requests
import ssl
import microcontroller
import alarm

i2c = busio.I2C(board.GP5, board.GP4)
sensor = INA219.INA219(i2c)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

url = "https://khm541kc10.execute-api.eu-west-1.amazonaws.com/dev/power"
wifi_ssid = os.getenv('CIRCUITPY_WIFI_SSID')
wifi_password = os.getenv('CIRCUITPY_WIFI_PASSWORD')


def Flash():
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)


try:
    Flash()

    print(f'Connecting to WiFi: {wifi_ssid}')

    wifi.radio.connect(wifi_ssid, wifi_password)

    pool = socketpool.SocketPool(wifi.radio)
    sslContext = ssl.create_default_context()
    requests = adafruit_requests.Session(pool, sslContext)

    Flash()
    Flash()
    print(f'Connected.')

    print("Taking sensor readings.")

    print("Voltage:\t\t{} V".format(sensor.bus_voltage))
    print("Current:\t\t{} mA".format(sensor.current))
    print("Power:\t\t\t{} W".format(sensor.power))

    print("Posting sensor readings.")

    response = requests.post(
        url, json={
            'deviceId': 0,
            'power': sensor.power,
        })

    print(f"Response: '{response.status_code}'.")

    if (response.status_code >= 200 and response.status_code < 300):
        Flash()
        Flash()
        Flash()

except Exception as e:
    print(f"An exception occurred {e}")

print("Sleep.")
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 480)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
