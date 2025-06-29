#!/usr/bin/env python3
import time
import bambulabs_api as bl
from dataclasses import asdict
import paho.mqtt.client as mqtt

import os

BAMBU_IP = os.environ.get("BAMBU_IP")
ACCESS_CODE = os.environ.get("ACCESS_CODE")
SERIAL = os.environ.get("SERIAL")
MQTT_BROKER = os.environ.get("MQTT_BROKER")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "10"))

# Setup MQTT
mqttc = mqtt.Client(protocol=mqtt.MQTTv311)
mqttc.connect(MQTT_BROKER, MQTT_PORT)

printer = bl.Printer(BAMBU_IP, ACCESS_CODE, SERIAL)
print(f"Connecting to {BAMBU_IP} with serial {SERIAL} and access code {ACCESS_CODE}")
printer.connect()

while True:
    try:
        bed_temp = printer.get_bed_temperature()
        nozzle_temp = printer.get_nozzle_temperature()
        chamber_temp = printer.get_chamber_temperature()
        wifi_signal_strength = printer.wifi_signal()
        print_speed = printer.get_print_speed()
        light_state = printer.get_light_state()
        current_file = printer.get_file_name()
        job_progress = printer.get_percentage()
        current_layer = printer.current_layer_num()
        total_layer = printer.total_layer_num()
        time_remaining = printer.get_time()

        # wait for first values to be ready
        # print("Waiting for printer telemetry to initialize...")
        # if bed_temp is None:
        #   print("Printer not ready, retrying...")
        #   time.sleep(POLL_INTERVAL)
        #   continue

        print("Attempting to publish telemetry data...")
        mqttc.publish("bambu/bed_temp", bed_temp)
        print(f"Bed temp: {bed_temp}")
        mqttc.publish("bambu/nozzle_temp", nozzle_temp)
        print(f"Nozzle temp: {nozzle_temp}")
        mqttc.publish("bambu/chamber_temp", chamber_temp)
        print(f"Chamber temp: {chamber_temp}")
        mqttc.publish("bambu/current_layer", current_layer)
        print(f"Current layer: {current_layer}")
        mqttc.publish("bambu/total_layer", total_layer)
        print(f"Total layers: {total_layer}")
        mqttc.publish("bambu/job_progress", job_progress)
        print(f"Job progress: {job_progress}")
        mqttc.publish("bambu/print_speed", print_speed)
        print(f"Print speed: {print_speed}")
        mqttc.publish("bambu/time_remaining", time_remaining)
        print(f"Time remaining: {time_remaining}")
        wifi_str = str(wifi_signal_strength).replace("dBm", "").strip()
        try:
            wifi_num = int(wifi_str)
        except (ValueError, TypeError):
            wifi_num = 0
        mqttc.publish("bambu/wifi_signal_strength", wifi_num)
        print(f"Wi-fi signal: {wifi_signal_strength}")
        mqttc.publish("bambu/current_file", current_file)
        print(f"Current file: {current_file}")
        light_num = 1 if light_state == "on" else 0
        mqttc.publish("bambu/light_state", light_num)
        print(f"Light state: {light_state}")
        print("Done publishing.")
    except Exception as e:
        print(f"Error polling printer: {e}")
    time.sleep(POLL_INTERVAL)