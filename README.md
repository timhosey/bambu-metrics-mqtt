# Bambu Metrics MQTT Bridge

This project provides a lightweight Python-based bridge that collects telemetry data from a Bambu Labs P1S 3D printer and publishes it to an MQTT broker. This allows the printer’s status and telemetry (bed temperature, nozzle temperature, job progress, and more) to be scraped into Prometheus and visualized in Grafana for advanced monitoring.

---

## Features

- Collects real-time Bambu Labs printer telemetry
- Publishes data to an MQTT broker for downstream processing
- Supports easy containerized deployment with Docker and Docker Compose
- Designed to integrate with Prometheus + Grafana for rich visualization

---

## Prerequisites

Before you begin, make sure you have:

- A Bambu Labs printer on your local network with LAN mode enabled
- Access to its IP address, serial number, and API access code
- A working MQTT broker (e.g. Mosquitto)
- Docker and Docker Compose installed on your deployment host
- (Optional) A Prometheus + Grafana stack to visualize and store the metrics

---

## Installation

1. **Clone this repository**

```bash
git clone https://github.com/your-org/bambu-metrics-mqtt.git
cd bambu-metrics-mqtt
```

2.	Configure environment variables

Edit docker-compose.yml and adjust these variables under the bambu_bridge service:
*	BAMBU_IP – IP address of your Bambu printer
*	ACCESS_CODE – API access code from the Bambu app/printer dashboard
*	SERIAL – the printer's serial number
*	MQTT_BROKER – your MQTT broker IP or hostname
*	MQTT_PORT – default 1883 unless you changed it
* POLL_INTERVAL – in seconds between telemetry polls

3.	Build and deploy
```bash
docker-compose build
docker-compose up -d
```

⸻

Usage

Once deployed, the bridge will continuously poll your printer’s telemetry and publish to the configured MQTT topics, e.g.:
	•	bambu/bed_temp
	•	bambu/nozzle_temp
	•	bambu/job_progress
	•	bambu/current_layer
	•	bambu/total_layer
	•	and others

You can then configure mqtt2prometheus or another MQTT-Prometheus bridge to scrape those topics and visualize them in Grafana.

⸻

Troubleshooting
	•	Ensure your printer is reachable on the network and the IP is correct
	•	Validate the MQTT broker is accessible from within the container (using network_mode: host if needed)
	•	Check your Prometheus scrape configuration points to the correct MQTT exporter port

For deeper support, please refer to the docker-compose logs and verify telemetry is flowing correctly with mosquitto_sub.

⸻

License

This project is licensed under the MIT License. See LICENSE for details.

⸻

Happy printing and monitoring!