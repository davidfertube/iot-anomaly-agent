import gradio as gr
import plotly.express as px
from src.anomaly_engine import anomaly_engine

def run_analysis():
    df = anomaly_engine.generate_sample_data()
    df = anomaly_engine.detect_anomalies(df)
    
    # Create plot
    fig = px.line(df, x="timestamp", y=["temperature", "pressure", "vibration"], title="Sensor Telemetry")
    
    # Highlight anomalies
    anomalies = df[df["is_anomaly"]]
    for idx, row in anomalies.iterrows():
        fig.add_annotation(x=row["timestamp"], y=row["temperature"], text="Anomaly", showarrow=True, arrowhead=1)

    # Analyze the most significant anomaly
    analysis = "No significant anomalies detected."
    if not anomalies.empty:
        analysis = anomaly_engine.analyze_root_cause(anomalies.tail(1))
    
    return fig, analysis

# ============================================
# GRADIO UI
# ============================================

with gr.Blocks(title="IoT Anomaly Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # IoT Anomaly Agent
    ### Turbine Anomaly Detection Agent
    
    Using **Isolation Forest** for detection and **Mistral-7B** for Root Cause Analysis (RCA).
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            plot_output = gr.Plot(label="Telemetry Stream")
        with gr.Column(scale=1):
            analysis_output = gr.Markdown(label="Root Cause Analysis")
            run_btn = gr.Button("Analyze Stream", variant="primary")
            
    run_btn.click(
        fn=run_analysis,
        inputs=[],
        outputs=[plot_output, analysis_output]
    )
    
    gr.Markdown("""
    ---
    **Tech Stack:** Isolation Forest • Mistral-7B • Plotly • Gradio
    
    **Author:** [David Fernandez](https://davidfernandez.dev) | AI Engineer
    """)

if __name__ == "__main__":
    demo.launch()
