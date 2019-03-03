from sensors import am2320, bmp280
from machine import I2C, Pin, Timer
import network
import sys
import urequests

sda = Pin(4, Pin.IN, Pin.PULL_UP)
scl = Pin(5, Pin.IN, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=50000)

sensor1 = am2320.AM2320(i2c)
sensor2 = bmp280.BMP280(i2c)

button = Pin(0, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)


def measure():
    try:
        sensor1.measure()
    except:
        pass


def toggle_led():
    if led.value() == 1:
        led.off()
    else:
        led.on()


measure()
sensor_timer = Timer(-1)
sensor_timer.init(period=5000, mode=Timer.PERIODIC, callback=lambda t: measure())

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("FBI Surveillance Van 4", "")

led_timer = Timer(-2)
led_timer.init(period=100, mode=Timer.PERIODIC, callback=lambda t: toggle_led())


def send_reading():
    urequests.post("http://192.168.1.103:3000", data={"value": sensor2.temperature, "sensor": "bmp280"})
    # urequests.post("http://192.168.1.103:3000", data = {"value": sensor2.pressure, "sensor": "bmp280"})
    urequests.post("http://192.168.1.103:3000", data={"value": sensor1.temperature(), "sensor": "am2320"})
    print("lol")


send_timer = Timer(-3)
send_timer.init(period=10000, mode=Timer.PERIODIC, callback=lambda t: send_reading())


def check_button():
    if button.value() == 0:
        print("EXIT")
        led.off()
        sys.exit()
    else:
        return 1


while not wifi.isconnected():
    check_button()
    continue

led_timer.deinit()
led.on()

# addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
#
# s = socket.socket()
# s.bind(addr)
# s.listen(1)


# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)


# response = urequests.post("http://192.168.1.103:3000", data = {"": ""})


while check_button():
    continue
