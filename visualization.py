# visualization.py - Real-time visualization and plotting
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class RealTimeVisualization:
    """Enhanced Real-time Visualization with Popup Alarms"""
    
    def __init__(self, simulator):
        self.simulator = simulator
        self.fig = None
        self.ax = None
        self.real_time_data = {}
        self.popup_alarms = []
        
    def create_realtime_dashboard(self):
        """Create real-time monitoring dashboard"""
        plt.ion()  # Interactive mode ON
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.suptitle("🚨 AI BORDER SECURITY - REAL-TIME MONITORING DASHBOARD", 
                         fontsize=16, fontweight='bold', color='darkred')
        
    def update_realtime_display(self):
        """Update real-time display with current data"""
        if self.fig is None:
            self.create_realtime_dashboard()
        
        self.ax.clear()
        
        # Draw all components
        self._draw_border_area()
        self._draw_sensor_nodes()
        self._draw_cluster_heads()
        self._draw_gateway()
        self._draw_intrusions()
        self._draw_communications()
        self._draw_popup_alarms()
        self._draw_real_time_data()
        
        plt.draw()
        plt.pause(0.1)
    
    def _draw_border_area(self):
        """Draw border area"""
        border = self.simulator
        self.ax.plot([0, border.border_length], [0, 0], 'r-', linewidth=4, label='BORDER LINE')
        self.ax.fill_between([0, border.border_length], 0, border.border_width, 
                           alpha=0.1, color='red', label='PROTECTED AREA')
        
        # Add distance markers
        for x in range(0, border.border_length + 1, 100):
            self.ax.text(x, -10, f'{x}m', ha='center', fontsize=8, alpha=0.7)
    
    def _draw_sensor_nodes(self):
        """Draw sensor nodes with real-time data"""
        border = self.simulator
        
        for node in border.sensor_nodes:
            color = 'green' if node.is_active else 'red'
            marker = 's' if node.has_camera else 'o'
            size = 80 if node.has_camera else 60
            
            # Node with camera has different style
            if node.has_camera:
                self.ax.scatter(node.x, node.y, c=color, marker=marker, s=size, 
                              edgecolors='black', linewidth=2, alpha=0.8)
                
                # Camera indicator
                if node.camera_status == "RECORDING":
                    self.ax.plot(node.x, node.y, 'ro', markersize=10, alpha=0.6)
            else:
                self.ax.scatter(node.x, node.y, c=color, marker=marker, s=size, 
                              alpha=0.7, edgecolors='black', linewidth=1)
            
            # Real-time data labels
            battery_text = f"{node.battery:.0f}%"
            battery_color = 'green' if node.battery > 50 else 'orange' if node.battery > 20 else 'red'
            
            self.ax.text(node.x, node.y + 8, battery_text, 
                       ha='center', fontsize=7, color=battery_color, weight='bold')
            
            # Node ID
            self.ax.text(node.x, node.y - 8, node.node_id, 
                       ha='center', fontsize=6, alpha=0.8)
            
            # Sensor activity indicator
            if node.sensor_readings['intrusion_detected']:
                self.ax.plot(node.x, node.y, 'r*', markersize=15, alpha=0.8)
    
    def _draw_cluster_heads(self):
        """Draw cluster heads with prediction data"""
        border = self.simulator
        
        for ch in border.cluster_heads:
            # Cluster head base
            self.ax.scatter(ch.x, ch.y, c='blue', marker='D', s=200, 
                          edgecolors='black', linewidth=2)
            
            # Prediction info
            if ch.prediction_history:
                latest = ch.prediction_history[-1]
                pred_text = f"CH{ch.node_id[-1]}\n{latest['prediction']}\n({latest['confidence']:.2f})"
                
                # Color based on prediction
                pred_color = 'red' if latest['prediction'] != 'normal' else 'green'
                
                self.ax.text(ch.x, ch.y + 15, pred_text, 
                           ha='center', fontsize=8, color=pred_color, weight='bold',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.8))
    
    def _draw_gateway(self):
        """Draw gateway/base station"""
        border = self.simulator
        gateway = border.gateway
        
        # Gateway base station
        self.ax.scatter(gateway.x, gateway.y, c='purple', marker='^', s=400, 
                      edgecolors='black', linewidth=3)
        
        # Gateway info box
        gateway_info = (
            f"🏠 BASE STATION\n"
            f"AI Gateway\n"
            f"Accuracy: {gateway.model_accuracy:.3f}\n"
            f"Alerts: {len(gateway.intrusion_alerts)}\n"
            f"Uptime: {border.simulation_time}s"
        )
        
        self.ax.text(gateway.x, gateway.y + 40, gateway_info, 
                   ha='center', fontsize=9, weight='bold',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.9))
    
    def _draw_intrusions(self):
        """Draw intrusion events"""
        try:
            border = self.simulator
            
            for intrusion in border.current_intrusions:
                color_map = {'human': 'red', 'vehicle': 'purple', 'animal': 'orange'}
                color = color_map.get(intrusion.get('type', 'human'), 'red')
                
                position_x = intrusion.get('position', 0)
                
                # Intrusion point
                self.ax.scatter(position_x, 0, c=color, marker='*', s=300, 
                              edgecolors='black', linewidth=2)
                
                # Detection zone
                detection_range = border.config["intrusion"]["detection_ranges"].get(
                    intrusion.get('type', 'human'), 50)
                circle = plt.Circle((position_x, 0), detection_range, 
                                  color=color, alpha=0.2, linestyle='--', linewidth=2)
                self.ax.add_patch(circle)
                
                # Intrusion info
                status = "DETECTED" if intrusion.get('detected', False) else "ACTIVE"
                affected_count = intrusion.get('affected_nodes', 0)
                intrusion_info = f"{intrusion.get('type', 'UNKNOWN').upper()} INTRUSION\n{status}\n{affected_count} nodes"
                
                self.ax.text(position_x, -25, intrusion_info, 
                           ha='center', fontsize=10, weight='bold', color=color,
                           bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow', alpha=0.8))
        except Exception as e:
            print(f"❌ Error drawing intrusions: {e}")
    
    def _draw_communications(self):
        """Draw communication links"""
        border = self.simulator
        
        # Sensor to cluster head links
        for node in border.sensor_nodes:
            if node.cluster_head_id and node.is_active:
                ch = next((ch for ch in border.cluster_heads if ch.node_id == node.cluster_head_id), None)
                if ch:
                    line_alpha = 0.3 if node.sensor_readings['signal_strength'] > 0.5 else 0.1
                    self.ax.plot([node.x, ch.x], [node.y, ch.y], 'gray', 
                               alpha=line_alpha, linewidth=0.5)
        
        # Cluster head to gateway links
        for ch in border.cluster_heads:
            self.ax.plot([ch.x, border.gateway.x], [ch.y, border.gateway.y], 'red', 
                       alpha=0.4, linewidth=1, linestyle='--')
    
    def _draw_popup_alarms(self):
        """Draw popup alarm messages"""
        border = self.simulator
        
        # Show latest alerts as popups
        if border.gateway.intrusion_alerts:
            latest_alert = border.gateway.intrusion_alerts[-1]
            
            # Popup alarm box
            alarm_text = (
                f"🚨 ALERT #{latest_alert['alert_id']}\n"
                f"Type: {latest_alert['intrusion_type'].upper()}\n"
                f"Confidence: {latest_alert['confidence']:.2f}\n"
                f"Severity: {latest_alert['severity']}\n"
                f"Time: {latest_alert['timestamp'].strftime('%H:%M:%S')}"
            )
            
            self.ax.text(border.border_length/2, border.border_width + 30, alarm_text,
                       ha='center', fontsize=12, weight='bold', color='red',
                       bbox=dict(boxstyle="round,pad=1", facecolor='lightcoral', alpha=0.9))
    
    def _draw_real_time_data(self):
        """Draw real-time data panel"""
        border = self.simulator
        
        # Real-time statistics panel
        active_nodes = sum(1 for n in border.sensor_nodes if n.is_active)
        avg_battery = np.mean([n.battery for n in border.sensor_nodes])
        camera_nodes = sum(1 for n in border.sensor_nodes if n.has_camera)
        recording_cameras = sum(1 for n in border.sensor_nodes if n.camera_status == "RECORDING")
        
        stats_text = (
            f"📊 REAL-TIME STATISTICS\n"
            f"Active Nodes: {active_nodes}/{len(border.sensor_nodes)}\n"
            f"Avg Battery: {avg_battery:.1f}%\n"
            f"Camera Nodes: {camera_nodes} ({recording_cameras} rec)\n"
            f"Intrusions: {len(border.current_intrusions)}\n"
            f"Alerts: {len(border.gateway.intrusion_alerts)}\n"
            f"Sim Time: {border.simulation_time}s"
        )
        
        self.ax.text(10, border.border_width - 20, stats_text,
                   fontsize=9, weight='bold', color='blue',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
        
        # Performance metrics
        if border.performance_metrics['total_intrusions'] > 0:
            detection_rate = (border.performance_metrics['detected_intrusions'] / 
                            border.performance_metrics['total_intrusions'])
            performance_text = f"Detection Rate: {detection_rate:.1%}"
            self.ax.text(border.border_length - 150, border.border_width - 20, performance_text,
                       fontsize=9, weight='bold', color='green' if detection_rate > 0.8 else 'orange',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # Set plot properties
        self.ax.set_xlabel('Border Length (meters)')
        self.ax.set_ylabel('Border Width (meters)')
        self.ax.set_title(f'AI-Enabled Border Security - Live Monitoring | '
                         f'Last Update: {datetime.now().strftime("%H:%M:%S")}', 
                         fontsize=14, weight='bold')
        self.ax.grid(True, alpha=0.3)
        self.ax.axis('equal')
        self.ax.set_ylim(-50, border.border_width + 50)
    
    def close_dashboard(self):
        """Close the visualization dashboard"""
        if self.fig:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
