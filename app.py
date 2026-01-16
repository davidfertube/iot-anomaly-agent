"""
IoT Anomaly Detection Agent
Real-time industrial sensor monitoring with AI-powered anomaly detection and automated work order generation.
"""

import gradio as gr
import numpy as np
import pandas as pd
import time
from datetime import datetime
import random

# Sensor configuration
SENSORS = {
    'wellhead_pressure': {'name': 'Wellhead Pressure', 'unit': 'PSI', 'min': 2000, 'max': 3500, 'warning': 2800, 'critical': 3200, 'icon': '⬆️'},
    'process_temp': {'name': 'Process Temperature', 'unit': '°F', 'min': 150, 'max': 250, 'warning': 210, 'critical': 235, 'icon': '️'},
    'flow_rate': {'name': 'Flow Rate', 'unit': 'BBL/D', 'min': 500, 'max': 1200, 'warning': 1000, 'critical': 1100, 'icon': ''},
    'pump_vibration': {'name': 'Pump Vibration', 'unit': 'mm/s', 'min': 0, 'max': 10, 'warning': 4.5, 'critical': 7.5, 'icon': ''},
    'h2s_level': {'name': 'H2S Level', 'unit': 'PPM', 'min': 0, 'max': 50, 'warning': 10, 'critical': 20, 'icon': '️'},
    'power_draw': {'name': 'Power Draw', 'unit': 'kW', 'min': 20, 'max': 80, 'warning': 55, 'critical': 70, 'icon': ''}
}

class IoTSimulator:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.values = {
            'wellhead_pressure': 2450,
            'process_temp': 185,
            'flow_rate': 850,
            'pump_vibration': 2.1,
            'h2s_level': 3,
            'power_draw': 42
        }
        self.history = {k: [] for k in SENSORS.keys()}
        self.logs = []
        self.work_order = None
        self.step = 0
        self.anomaly_injected = False
    
    def get_status(self, sensor_id, value):
        config = SENSORS[sensor_id]
        if value >= config['critical']:
            return 'CRITICAL'
        elif value >= config['warning']:
            return 'WARNING'
        return 'NORMAL'
    
    def add_log(self, message, level='INFO'):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.logs.append(f"[{timestamp}] [{level}] {message}")
        if len(self.logs) > 15:
            self.logs = self.logs[-15:]
    
    def inject_anomaly(self):
        """Simulate a pump bearing failure scenario"""
        self.anomaly_injected = True
        self.add_log("️ Anomaly injection started - simulating pump bearing failure", "WARN")
    
    def step_simulation(self):
        self.step += 1
        
        # Normal random variation
        for sensor_id in self.values:
            config = SENSORS[sensor_id]
            noise = np.random.normal(0, (config['max'] - config['min']) * 0.01)
            self.values[sensor_id] = max(config['min'], min(config['max'], self.values[sensor_id] + noise))
        
        # Anomaly progression
        if self.anomaly_injected:
            progression = min(1.0, (self.step - 5) / 10)  # Gradual increase
            
            # Vibration increases first
            if self.step > 5:
                self.values['pump_vibration'] = 2.1 + progression * 6.5
                if self.get_status('pump_vibration', self.values['pump_vibration']) == 'WARNING':
                    self.add_log(f"️ Pump Vibration elevated: {self.values['pump_vibration']:.1f} mm/s", "WARN")
                elif self.get_status('pump_vibration', self.values['pump_vibration']) == 'CRITICAL':
                    self.add_log(f" CRITICAL: Pump Vibration at {self.values['pump_vibration']:.1f} mm/s", "CRITICAL")
            
            # Temperature follows
            if self.step > 8:
                self.values['process_temp'] = 185 + progression * 55
                if self.get_status('process_temp', self.values['process_temp']) == 'WARNING':
                    self.add_log(f"️ Process Temperature elevated: {self.values['process_temp']:.0f}°F", "WARN")
            
            # Power draw increases
            if self.step > 10:
                self.values['power_draw'] = 42 + progression * 30
                if self.get_status('power_draw', self.values['power_draw']) == 'WARNING':
                    self.add_log(f"️ Power Draw increased: {self.values['power_draw']:.0f} kW", "WARN")
            
            # Generate work order when pattern is detected
            if self.step == 15 and not self.work_order:
                self.add_log(" Anomaly pattern detected: Pump bearing failure signature", "DETECT")
                self.add_log(" AI Agent initiating automated response workflow...", "ACTION")
                time.sleep(0.5)
                self.add_log(" Generating maintenance work order...", "ACTION")
                self.work_order = {
                    'id': f'WO-{random.randint(100000, 999999)}',
                    'asset': 'Pump Station P-101',
                    'issue': 'Bearing failure detected',
                    'priority': 'URGENT',
                    'eta': '~4 hours to failure',
                    'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.add_log(f" Work Order {self.work_order['id']} created and sent to on-call engineer", "SUCCESS")
        
        # Update history
        for sensor_id in self.values:
            self.history[sensor_id].append(self.values[sensor_id])
            if len(self.history[sensor_id]) > 20:
                self.history[sensor_id] = self.history[sensor_id][-20:]
        
        return self.get_dashboard_data()
    
    def get_dashboard_data(self):
        # Create sensor cards HTML
        sensor_html = '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1rem;">'
        for sensor_id, value in self.values.items():
            config = SENSORS[sensor_id]
            status = self.get_status(sensor_id, value)
            
            if status == 'CRITICAL':
                bg_color = 'rgba(239, 68, 68, 0.2)'
                border_color = '#ef4444'
                value_color = '#ef4444'
            elif status == 'WARNING':
                bg_color = 'rgba(245, 158, 11, 0.2)'
                border_color = '#f59e0b'
                value_color = '#f59e0b'
            else:
                bg_color = 'rgba(16, 185, 129, 0.1)'
                border_color = '#10b981'
                value_color = '#10b981'
            
            display_value = f"{value:.1f}" if isinstance(value, float) and value % 1 != 0 else f"{int(value)}"
            
            sensor_html += f'''
            <div style="background: {bg_color}; border: 2px solid {border_color}; border-radius: 12px; padding: 1rem; text-align: center;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{config['icon']}</div>
                <div style="font-size: 0.75rem; color: #888; text-transform: uppercase;">{config['name']}</div>
                <div style="font-size: 1.5rem; font-weight: bold; color: {value_color};">{display_value}</div>
                <div style="font-size: 0.7rem; color: #888;">{config['unit']}</div>
            </div>
            '''
        sensor_html += '</div>'
        
        # Create logs HTML
        logs_html = '<div style="background: #1a1a2e; border-radius: 8px; padding: 1rem; font-family: monospace; font-size: 0.8rem; max-height: 200px; overflow-y: auto;">'
        for log in self.logs[-10:]:
            if 'CRITICAL' in log:
                color = '#ef4444'
            elif 'WARN' in log or '️' in log:
                color = '#f59e0b'
            elif 'SUCCESS' in log or '' in log:
                color = '#10b981'
            elif 'ACTION' in log or '' in log:
                color = '#8b5cf6'
            else:
                color = '#888'
            logs_html += f'<div style="color: {color}; margin-bottom: 0.25rem;">{log}</div>'
        logs_html += '</div>'
        
        # Create work order HTML
        if self.work_order:
            work_order_html = f'''
            <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.1)); border: 1px solid #6366f1; border-radius: 12px; padding: 1rem; margin-top: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-weight: bold;"> Work Order Generated</span>
                    <span style="background: rgba(99, 102, 241, 0.3); padding: 0.25rem 0.5rem; border-radius: 4px; font-family: monospace; font-size: 0.75rem;">{self.work_order['id']}</span>
                </div>
                <div style="display: grid; gap: 0.25rem; font-size: 0.85rem;">
                    <div><span style="color: #888;">Asset:</span> {self.work_order['asset']}</div>
                    <div><span style="color: #888;">Issue:</span> {self.work_order['issue']}</div>
                    <div><span style="color: #888;">Priority:</span> <span style="color: #ef4444; font-weight: bold;">{self.work_order['priority']}</span></div>
                    <div><span style="color: #888;">ETA:</span> {self.work_order['eta']}</div>
                </div>
            </div>
            '''
        else:
            work_order_html = ''
        
        return sensor_html, logs_html, work_order_html

# Global simulator instance
simulator = IoTSimulator()

def run_simulation(progress=gr.Progress()):
    """Run the full anomaly detection simulation"""
    simulator.reset()
    simulator.add_log(" Connecting to Azure IoT Hub...", "INFO")
    yield simulator.get_dashboard_data()
    time.sleep(0.5)
    
    simulator.add_log(" Receiving telemetry from 6 sensors", "INFO")
    yield simulator.get_dashboard_data()
    time.sleep(0.5)
    
    simulator.add_log(" AI Agent monitoring initialized", "INFO")
    yield simulator.get_dashboard_data()
    time.sleep(0.5)
    
    # Normal operation for a few steps
    for i in range(5):
        simulator.step_simulation()
        yield simulator.get_dashboard_data()
        time.sleep(0.3)
    
    # Inject anomaly
    simulator.inject_anomaly()
    
    # Run anomaly progression
    for i in range(15):
        simulator.step_simulation()
        yield simulator.get_dashboard_data()
        time.sleep(0.4)
    
    return simulator.get_dashboard_data()

def reset_simulation():
    """Reset the simulation to initial state"""
    simulator.reset()
    return simulator.get_dashboard_data()

# Create Gradio interface
with gr.Blocks(title="IoT Anomaly Detection Agent", theme=gr.themes.Soft(primary_hue="indigo")) as demo:
    gr.Markdown("""
    #  IoT Anomaly Detection Agent
    **Real-time industrial sensor monitoring with AI-powered anomaly detection and automated work order generation**
    
    This demo simulates a pump bearing failure scenario where the AI agent:
    1. Monitors 6 sensor types in real-time
    2. Detects multi-sensor anomaly patterns
    3. Automatically generates maintenance work orders
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            sensor_output = gr.HTML(label="Sensor Dashboard")
            
            gr.Markdown("###  Architecture")
            gr.Markdown("`Sensors → Azure IoT Hub → Stream Analytics → Anomaly ML → Sim.ai Agent → Work Order`")
        
        with gr.Column(scale=1):
            gr.Markdown("###  Agent Log")
            logs_output = gr.HTML(label="Agent Activity")
            work_order_output = gr.HTML(label="Work Order")
    
    with gr.Row():
        run_btn = gr.Button("▶️ Run Simulation", variant="primary", size="lg")
        reset_btn = gr.Button(" Reset", variant="secondary")
    
    # Event handlers
    run_btn.click(
        fn=run_simulation,
        outputs=[sensor_output, logs_output, work_order_output]
    )
    
    reset_btn.click(
        fn=reset_simulation,
        outputs=[sensor_output, logs_output, work_order_output]
    )
    
    # Initialize on load
    demo.load(
        fn=reset_simulation,
        outputs=[sensor_output, logs_output, work_order_output]
    )
    
    gr.Markdown("""
    ---
    **Author:** David Fernandez | [Website](https://davidfernandez.dev) | [GitHub](https://github.com/davidfertube)
    
    *Built with Azure IoT Hub (Free Tier), Sim.ai, and Gradio*
    """)

if __name__ == "__main__":
    demo.launch()
