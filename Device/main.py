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

i2c0 = busio.I2C(board.GP5, board.GP4)
loadSensor = INA219.INA219(i2c0, 64)
solarPanelSensor = INA219.INA219(i2c0, 65)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

url = "https://khm541kc10.execute-api.eu-west-1.amazonaws.com/dev/power"
wifi_ssid = os.getenv('CIRCUITPY_WIFI_SSID')
wifi_password = os.getenv('CIRCUITPY_WIFI_PASSWORD')


def Flash(duration: float, flashes: int):
    for x in range(flashes):
        led.value = True
        time.sleep(duration)
        led.value = False
        time.sleep(duration)


try:
    time.sleep(2)

    Flash(0.5, 1)

    print(f'Connecting to WiFi: {wifi_ssid}')

    wifi.radio.connect(wifi_ssid, wifi_password)

    pool = socketpool.SocketPool(wifi.radio)
    sslContext = ssl.create_default_context()
    requests = adafruit_requests.Session(pool, sslContext)

    Flash(0.5, 2)

    print(f'Connected.')

    print("Taking load sensor readings.")
    print("Voltage:\t\t{} V".format(loadSensor.shunt_voltage))
    print("Current:\t\t{} mA".format(loadSensor.current))
    print("Power:\t\t\t{} W".format(loadSensor.power))

    print("Taking solar sensor readings.")
    print("Voltage:\t\t{} V".format(solarPanelSensor.shunt_voltage))
    print("Current:\t\t{} mA".format(solarPanelSensor.current))
    print("Power:\t\t\t{} W".format(solarPanelSensor.power))

    print("Posting sensor readings.")

    response = requests.post(
        url, json={
            'deviceId': 0,
            'loadPower': loadSensor.power,
            'loadCurrent': loadSensor.current,
            'solarPower': solarPanelSensor.power,
            'solarVoltage': solarPanelSensor.shunt_voltage,
            'solarCurrent': solarPanelSensor.current,
        })

    print(f"Response: '{response.status_code}'.")

    if (response.status_code >= 200 and response.status_code < 300):
        Flash(0.5, 3)

except Exception as e:
    print(f"An exception occurred {e}")

print("Sleep.")
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 240)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
