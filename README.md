# Anomaly Agent

**Real-Time Turbine Anomaly Detection with Automated Root Cause Analysis**

Isolation Forest-based anomaly detection for gas turbine sensor streams, paired with LLM-powered root cause analysis that translates statistical outliers into actionable maintenance diagnostics.

[![Live Demo](https://img.shields.io/badge/Live_Demo-HuggingFace-yellow?style=flat-square)](https://huggingface.co/spaces/davidfertube/anomaly-agent)
[![Portfolio](https://img.shields.io/badge/Portfolio-davidfernandez.dev-00d4ff?style=flat-square)](https://davidfernandez.dev/projects/anomaly-agent)

---

## Problem

Gas turbines in power generation and compression service produce hundreds of sensor readings per second across vibration, temperature, pressure, and flow channels. Operators face two challenges:

1. **Volume**: A single GE Frame 7FA generates 200+ sensor channels. Manual monitoring is impossible at scale across a fleet of 10-50 units
2. **Subtlety**: The most expensive failures (bearing degradation, compressor blade fouling, hot gas path erosion) manifest as correlated multi-sensor drift weeks before catastrophic failure. Single-sensor threshold alarms miss these patterns entirely
3. **Interpretation**: When anomalies are detected, translating statistical deviations into maintenance actions requires deep domain expertise. A vibration spike at 147Hz means nothing without context (bearing defect frequency for that shaft speed)

## Solution

Two-stage system combining unsupervised anomaly detection with LLM-based diagnostic reasoning:

1. **Isolation Forest** trained on normal operating data isolates anomalous sensor combinations in real-time. The model flags multi-variate deviations that single-channel alarms would miss
2. **LLM root cause agent** (Mistral 7B) receives the anomaly context (which sensors deviated, by how much, operating conditions) and generates a plain-language diagnosis with recommended actions

**Key design decisions:**

- **Isolation Forest over autoencoders**: For this application, interpretability matters more than reconstruction accuracy. Isolation Forest provides anomaly scores per sample and feature importance, which feed directly into the RCA agent's context
- **Unsupervised training**: Labeled failure data is scarce in power generation. Isolation Forest only needs normal operating data, which is abundant from SCADA historians
- **LLM for RCA, not detection**: The statistical model handles detection (fast, deterministic). The LLM handles interpretation (contextual, flexible). This separation prevents LLM hallucination from affecting detection reliability
- **SCADA-native interface**: Sensor data ingestion follows OPC-UA / Modbus conventions. No custom telemetry protocol required

## Architecture

```
Turbine SCADA / Historian
         │
         ▼
┌──────────────────────────┐
│  Sensor Preprocessing     │  Normalization, window aggregation
│  Feature Engineering      │  Rolling stats, correlation features
└──────────┬───────────────┘
           ▼
┌──────────────────────────┐
│  Isolation Forest         │  Unsupervised anomaly scoring
│  (scikit-learn)           │  Per-feature importance
└──────────┬───────────────┘
           ▼
    ┌──────┴──────┐
    │  Anomaly?   │
    │  Score > θ  │
    └──────┬──────┘
           ▼ Yes
┌──────────────────────────┐
│  LLM Root Cause Agent     │  Mistral 7B via Groq
│  Context: sensor deltas,  │  Operating conditions,
│  equipment specs           │  Historical patterns
└──────────┬───────────────┘
           ▼
┌──────────────────────────┐
│  Operations Alert         │  Diagnosis + severity + action
│  Gradio Dashboard         │  Real-time visualization
└──────────────────────────┘
```

## Performance

| Metric | Value | Context |
|--------|-------|---------|
| Detection Latency | <15s | From sensor reading to anomaly flag |
| Sensor Channels | Multi-variate | Vibration, temperature, pressure, flow |
| Root Cause Analysis | Automated | LLM-generated diagnostics |
| SCADA Integration | OPC-UA | Standard industrial protocol |

## Tech Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Detection | Isolation Forest (scikit-learn) | Unsupervised, interpretable, fast inference |
| RCA Agent | Mistral 7B (Groq) | Low-latency LLM for contextual diagnostics |
| UI | Gradio | Interactive sensor simulation dashboard |
| Data Processing | Pandas, NumPy | Time-series preprocessing and windowing |
| Deployment | Docker | Containerized for edge or cloud deployment |

## Getting Started

```bash
git clone https://github.com/davidfertube/iot-anomaly-agent.git
cd iot-anomaly-agent

pip install -r requirements.txt

cp .env.example .env
# Add your Groq API key for the RCA agent

python app.py
```

## License

MIT License - 2026 David Fernandez

## Author

**David Fernandez** — Senior AI Engineer

- [Portfolio](https://davidfernandez.dev)
- [LinkedIn](https://linkedin.com/in/davidfertube)
- [GitHub](https://github.com/davidfertube)
