#!/usr/bin/env python3

import asyncio, time
import logging
import paho.mqtt.client as mqtt
from sys import argv
from growattRS232 import GrowattRS232


# defaults
# USB port of RS232 converter
DEFAULT_PORT = "/dev/ttyUSB0"
# Growatt modbus address
DEFAULT_ADDRESS = 0x1

logging.basicConfig(level=logging.DEBUG)

def on_connect (client, userdata, flags, rc):
  print("Connected with the result code"+str(rc))

async def main():
  port = str(argv[1]) if len(argv) > 1 else DEFAULT_PORT
  address = int(argv[2]) if len(argv) > 2 else DEFAULT_ADDRESS
  growattRS232 = GrowattRS232(port, address)
  mqttClient=mqtt.Client()
  mqttClient.on_connect = on_connect
  mqttClient.connect("monique.linaus.int", 1883, 60)
  
  while True :
    try:
      data = await growattRS232.async_update()
      #print(f"Sensors data: {data}")
      for entry in data:
        for item in entry:
        #mqttClient.publish("growatt/"+)
          print("Entry {entry} - {item}")
    except Exception as error:
      print("Error: " + repr(error))
      time.sleep(60)


loop = asyncio.get_event_loop()  
loop.run_until_complete(main())
loop.close()

# Sensors data: {'serial_number': 'QQ14490081', 
# 'model_number': 'T0 Q0 P15 U1 M5 S3',
# 'firmware': 'S.1.8\x00',
# 'input_power': 2568.6,
# 'input_energy_total': 47970.9,
# 'output_power': 2492.1,
# 'output_energy_today': 6.3,
# 'output_energy_total': 46431.1,
# 'output_reactive_power': 0.0,
# 'output_reactive_energy_today': 0.0,
# 'output_reactive_energy_total': 0.0,
# 'input_1_voltage': 275.4,
# 'input_1_amperage': 5.4,
# 'input_1_power': 1500.8, 
# 'input_1_energy_today': 4.0,
# 'input_1_energy_total': 25356.8, 
# 'input_2_voltage': 286.6, 
# 'input_2_amperage': 3.6, 
# 'input_2_power': 1067.8, 
# 'input_2_energy_today': 2.4, 
# 'input_2_energy_total': 22614.1, 
# 'output_1_voltage': 244.0, 
# 'output_1_amperage': 9.8, 
# 'output_1_power': 2492.1, 
# 'output_2_voltage': 0.0, 
# 'output_2_amperage': 0.0, 
# 'output_2_power': 0.0, 
# 'output_3_voltage': 0.0, 
# 'output_3_amperage': 0.0, 
# 'output_3_power': 0.0, 
# 'operation_hours': 29480.38611111111, 
# 'frequency': 49.97, 
# 'temperature': 35.1, 
# 'ipm_temperature': 0.0, 
# 'p_bus_voltage': 405.2, 
# 'n_bus_voltage': 0.0, 
# 'derating_mode': 0, 
# 'derating': 'No Deratring', 
# 'status_code': 1, 
# 'status': 'Normal', 
# 'fault_code': 0, 
# 'fault': 'None', 
# 'warning_code': 0, 
# 'warning': 'None', 
# 'warning_value': 0}
