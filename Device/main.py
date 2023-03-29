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

i2c = busio.I2C(board.GP5, board.GP4)
sensor = INA219.INA219(i2c)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

location = "Preston, GB"
# openweathermap URL, brings in your location & your token
url = "https://api.openweathermap.org/data/2.5/weather?lat=53.6535&lon=-2.6326"
url += "&appid="+os.getenv('openweather_token')


print()
print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'),
                   os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
sslContext = ssl.create_default_context()
requests = adafruit_requests.Session(pool, sslContext)

while True:
    #  pings openweather
    response = requests.get("http://192.168.0.17:8000/?name=John")
    #  packs the response into a JSON
    response_as_json = response.json()
    print()
    #  prints the entire JSON
    print(response_as_json)

    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)
    print("Voltage:\t\t{} V".format(sensor.bus_voltage))
    print("Current:\t\t{} mA".format(sensor.current))
    print("Power:\t\t\t{} W".format(sensor.power))
    print("\n\r")

    time.sleep(20)
