import time
import adafruit_dht
import paho.mqtt.client as mqtt

import prometheus_client as prom

from gpiozero import Button
from datetime import datetime

# Debug
DEBUG = False

# Time between scrapes (in seconds)
LOOP_TIME = 59

# MQTT hostname
MQTT_SERVER = 'mqtt.local'
MQTT_USER = 'iot_user'
MQTT_PASS = 'iioott_pass'

# Temperature and Humidity sensor is DHT22 on GPIO4
DHT_PIN = 4

# Relay pin is GPIO21
RELAY = Button(21)
TP160 = 1
TP100 = 0


def log(msg):
    if DEBUG:
        now = datetime.now()
        print(f'{now:%Y-%m-%d %H:%M:%S}  {msg}')

# DHT22 initialization part
dht = adafruit_dht.DHT22(DHT_PIN)

# MQTT init/connect part
mqttc = mqtt.Client()
mqttc.username_pw_set(MQTT_USER, password=MQTT_PASS)
mqttc.connect(MQTT_SERVER)
mqttc.loop_start()

# Prometheus stuff
g_temp = prom.Gauge('temperature', 'Temperature, *C')
g_humid = prom.Gauge('humidity', 'Humidity, %')
g_ps = prom.Gauge('powersource', 'The source of electricity (1 - TP-160, 0 - TP-100)')


prom.start_http_server(9865)

# Collect loop
while True:
    # Relay state query
    if RELAY.is_pressed:
        psource = TP100
    else:
        psource = TP160

    # DHT22 query
    temperature = dht.temperature
    humidity = dht.humidity

    log(f'Power source: {psource}  '
        f'Temp: {temperature:.2f}*C  '
        f'Humidity: {humidity:.2f}')

    # MQTT part
    mqttc.publish('asm/sweethome/pole/temperature', temperature)
    mqttc.publish('asm/sweethome/pole/humidity', humidity)
    mqttc.publish('asm/sweethome/pole/powersource', psource)


    # Prometheus stuff
    g_temp.set(temperature)
    g_humid.set(humidity)
    g_ps.set(psource)

    # Global pause between scrapes of metrics
    time.sleep(LOOP_TIME)
