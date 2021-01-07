# pole_exporter

Prometheus exporter for electricity data from Raspberry PI near the electricity counter on the pole

## Exported Prometheus metrics:
- temperature and humidity from DHT-22 sensor
- the state of electricity switch (the source of electricity - `main` or `supplemental`) -- from gpio


## Additional functionality:
Publish metrics to the MQTT server (HomeAssistant support)

