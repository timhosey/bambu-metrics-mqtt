#!/usr/bin/env python3
import time
import os
import bambulabs_api as bl
from prometheus_client import start_http_server, Gauge

# Customize these:
BAMBU_IP = os.environ.get("BAMBU_IP")
ACCESS_CODE = os.environ.get("ACCESS_CODE")
SERIAL = os.environ.get("SERIAL")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "10"))

# These are for testing, so remove when final:
# BAMBU_IP = "192.168.0.76"
# ACCESS_CODE = "16845074"
# SERIAL = "01P00A433000756"
# POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "10"))

# Define Prometheus Gauges
bed_temp_gauge = Gauge('bambu_bed_temp', 'Bambu Bed Temperature')
nozzle_temp_gauge = Gauge('bambu_nozzle_temp', 'Bambu Nozzle Temperature')
chamber_temp_gauge = Gauge('bambu_chamber_temp', 'Bambu Chamber Temperature')
current_layer_gauge = Gauge('bambu_current_layer', 'Bambu Current Layer Number')
total_layer_gauge = Gauge('bambu_total_layer', 'Bambu Total Layer Number')
job_progress_gauge = Gauge('bambu_job_progress', 'Bambu Job Progress Percentage')
print_speed_gauge = Gauge('bambu_print_speed', 'Bambu Print Speed')
time_remaining_gauge = Gauge('bambu_time_remaining', 'Bambu Time Remaining')
wifi_signal_strength_gauge = Gauge('bambu_wifi_signal_strength', 'Bambu WiFi Signal Strength (dBm)')
light_state_gauge = Gauge('bambu_light_state', 'Bambu Light State (1=on, 0=off)')

start_http_server(int(os.environ.get("PROMETHEUS_PORT", "8000")))

printer = bl.Printer(BAMBU_IP, ACCESS_CODE, SERIAL)
printer.connect()

# wait for first values to be ready
print("Waiting for printer telemetry to initialize...")
wifi_signal_strength = printer.wifi_signal()
while wifi_signal_strength == '':
    print(f"Printer not ready, retrying. [Wifi Signal: {wifi_signal_strength}]")
    wifi_signal_strength = printer.wifi_signal()
    time.sleep(2)

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

        print("Setting Prometheus gauge metrics...")
        bed_temp_gauge.set(float(bed_temp) if bed_temp is not None else 0.0)
        print(f"Bed temp: {bed_temp}")
        nozzle_temp_gauge.set(float(nozzle_temp) if nozzle_temp is not None else 0.0)
        print(f"Nozzle temp: {nozzle_temp}")
        chamber_temp_gauge.set(float(chamber_temp) if chamber_temp is not None else 0.0)
        print(f"Chamber temp: {chamber_temp}")
        current_layer_gauge.set(int(current_layer) if current_layer is not None else 0)
        print(f"Current layer: {current_layer}")
        total_layer_gauge.set(int(total_layer) if total_layer is not None else 0)
        print(f"Total layers: {total_layer}")
        job_progress_gauge.set(float(job_progress) if job_progress is not None else 0.0)
        print(f"Job progress: {job_progress}")
        print_speed_gauge.set(float(print_speed) if print_speed is not None else 0.0)
        print(f"Print speed: {print_speed}")
        time_remaining_gauge.set(float(time_remaining) if time_remaining is not None else 0.0)
        print(f"Time remaining: {time_remaining}")
        try:
            wifi_num = int(str(wifi_signal_strength).replace("dBm","").strip())
        except Exception:
            wifi_num = 0
        wifi_signal_strength_gauge.set(wifi_num)
        print(f"Wi-fi signal: {wifi_num}")
        light_num = 1 if light_state == "on" else 0
        light_state_gauge.set(light_num)
        print(f"Light state: {light_state}")
        print("Done setting metrics.")
    except Exception as e:
        print(f"Error polling printer: {e}")
        printer.disconnect()
    time.sleep(POLL_INTERVAL)