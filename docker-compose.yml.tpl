version: "3.9"

services:
  bambu_bridge:
    build: .
    container_name: bambu_bridge
    restart: unless-stopped
    environment:
      - BAMBU_IP=192.168.50.199
      - ACCESS_CODE=12345678
      - SERIAL=01P00A123456789
      - MQTT_BROKER=1.2.3.4
      - MQTT_PORT=1883
      - POLL_INTERVAL=10
    network_mode: host