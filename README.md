---
title: IoT Anomaly Agent
emoji: 🤖
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: true
license: mit
short_description: Real-time IoT anomaly detection with AI agents
---

# IoT Anomaly Detection Agent

Real-time anomaly detection and automated response using AI agents for industrial sensor monitoring.

## Features
- **6 Sensor Types**: Wellhead pressure, process temperature, flow rate, pump vibration, H2S level, power draw
- **Real-time Anomaly Detection**: Multi-sensor pattern recognition
- **Automated Work Orders**: Auto-generate maintenance tickets
- **Human-in-the-Loop**: Configurable approval workflows

## Architecture
```
Sensors → Azure IoT Hub → Stream Analytics → Anomaly ML → Sim.ai Agent → Work Order
```

## Technology Stack
- Azure IoT Hub (Free Tier)
- Sim.ai Visual Agent Builder
- Isolation Forest + LSTM Autoencoder
- ServiceNow/Teams Integration

## Author
David Fernandez - Industrial AI Engineer
- Website: [davidfernandez.dev](https://davidfernandez.dev)
- GitHub: [davidfertube](https://github.com/davidfertube)
