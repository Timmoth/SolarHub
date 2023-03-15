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
requests = adafruit_requests.Session(pool, ssl.create_default_context())


while True:
    try:
        #  pings openweather
        response = requests.get(url)
        #  packs the response into a JSON
        response_as_json = response.json()
        print()
        #  prints the entire JSON
        print(response_as_json)
        #  gets location name
        place = response_as_json['name']
        #  gets weather type (clouds, sun, etc)
        weather = response_as_json['weather'][0]['main']
        #  gets humidity %
        humidity = response_as_json['main']['humidity']
        #  gets air pressure in hPa
        pressure = response_as_json['main']['pressure']
        #  gets temp in kelvin
        temperature = response_as_json['main']['temp']
        #  converts temp from kelvin to C
        converted_temp = (temperature - 273.15)

        #  prints out weather data formatted nicely as pulled from JSON
        print()
        print("The current weather in %s is:" % place)
        print(weather)
        print("%s°F" % converted_temp)
        print("%s%% Humidity" % humidity)
        print("%s hPa" % pressure)
        #  delay for 5 minutes
        time.sleep(300)
    # pylint: disable=broad-except
    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        time.sleep(20)

    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)
    print("Voltage:\t\t{} V".format(sensor.bus_voltage))
    print("Current:\t\t{} mA".format(sensor.current))
    print("Power:\t\t\t{} W".format(sensor.power))
    print("\n\r")
