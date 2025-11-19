# models.py - Complete with both SensorNode and ClusterHead classes
import numpy as np
import random
from datetime import datetime
from camera_module import CameraModule

class SensorNode:
    """Enhanced Wireless Sensor Node with Real-time Monitoring"""
    
    def __init__(self, node_id, x, y, config, node_type="sensor", has_camera=False):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.config = config
        self.node_type = node_type
        self.has_camera = has_camera
        self.is_active = True
        self.battery = random.uniform(config["energy"]["initial_battery_min"], 
                                    config["energy"]["initial_battery_max"])
        self.cluster_head_id = None
        self.last_update = datetime.now()
        
        # Initialize sensor readings
        self.sensor_readings = {
            'pir': 0,
            'vibration': 0,
            'thermal': 25.0,
            'acoustic': 0,
            'signal_strength': random.uniform(0.5, 1.0),
            'intrusion_detected': False
        }
        
        # Camera module (if available)
        self.camera_module = CameraModule(self) if has_camera else None
        self.camera_status = "IDLE"  # Camera status tracking
        
        # Data history for analytics
        self.data_history = []
        
        # Real-time sensor data streams
        self.sensor_stream = {
            'pir_history': [],
            'vibration_history': [],
            'thermal_history': [],
            'acoustic_history': [],
            'max_history_length': 50
        }

    def get_real_time_sensor_data(self):
        """Get real-time sensor data with timestamps"""
        current_time = datetime.now()
        
        sensor_data = {
            'node_id': self.node_id,
            'timestamp': current_time,
            'position': (self.x, self.y),
            'battery': round(self.battery, 1),
            'sensors': {
                'pir': self.sensor_readings['pir'],
                'vibration': self.sensor_readings['vibration'],
                'thermal': self.sensor_readings['thermal'],
                'acoustic': self.sensor_readings['acoustic'],
                'signal_strength': self.sensor_readings['signal_strength'],
                'max_temp_since_last_check': np.max(self.sensor_stream['thermal_history']) if self.sensor_stream['thermal_history'] else 25.0 # NEW DATA FIELD
            },
            'status': {
                'active': self.is_active,
                'camera_available': self.has_camera,
                'camera_status': self.camera_status,
                'intrusion_detected': self.sensor_readings['intrusion_detected']
            }
        }
        
        # Update sensor history
        self._update_sensor_history()
        
        return sensor_data
    
    def _update_sensor_history(self):
        """Update sensor data history for trends"""
        self.sensor_stream['pir_history'].append(self.sensor_readings['pir'])
        self.sensor_stream['vibration_history'].append(self.sensor_readings['vibration'])
        self.sensor_stream['thermal_history'].append(self.sensor_readings['thermal'])
        self.sensor_stream['acoustic_history'].append(self.sensor_readings['acoustic'])
        
        # Keep history within limits
        for key in ['pir_history', 'vibration_history', 'thermal_history', 'acoustic_history']:
            if len(self.sensor_stream[key]) > self.sensor_stream['max_history_length']:
                self.sensor_stream[key].pop(0)
    
    def get_sensor_trends(self):
        """Get sensor data trends over time"""
        trends = {}
        
        for sensor_type in ['pir', 'vibration', 'thermal', 'acoustic']:
            history = self.sensor_stream[f'{sensor_type}_history']
            if history:
                trends[sensor_type] = {
                    'current': history[-1],
                    'average': np.mean(history),
                    'max': np.max(history),
                    'min': np.min(history),
                    'trend': 'increasing' if len(history) > 1 and history[-1] > history[-2] else 'decreasing'
                }
        
        return trends
    
    def simulate_sensor_fault(self, fault_type=None):
        """Simulate sensor faults for testing"""
        if fault_type == "random":
            # Random sensor failure
            if random.random() < 0.05:  # 5% chance of fault
                fault_sensor = random.choice(['pir', 'vibration', 'thermal', 'acoustic'])
                self.sensor_readings[fault_sensor] = 0
                print(f"🔧 Sensor {fault_sensor} fault simulated on {self.node_id}")
        
        elif fault_type == "battery_low":
            # Simulate low battery effects
            if self.battery < 20:
                for sensor in ['vibration', 'acoustic']:
                    self.sensor_readings[sensor] *= 0.5  # Reduced sensitivity
    
    def get_sensor_health_report(self):
        """Generate sensor health report"""
        return {
            'node_id': self.node_id,
            'battery_health': 'GOOD' if self.battery > 50 else 'LOW' if self.battery > 20 else 'CRITICAL',
            'signal_health': 'STRONG' if self.sensor_readings['signal_strength'] > 0.7 else 'WEAK',
            'sensor_status': {
                'pir': 'ACTIVE' if self.sensor_readings['pir'] >= 0 else 'FAULTY',
                'vibration': 'ACTIVE' if self.sensor_readings['vibration'] >= 0 else 'FAULTY',
                'thermal': 'ACTIVE' if 15 <= self.sensor_readings['thermal'] <= 50 else 'FAULTY',
                'acoustic': 'ACTIVE' if self.sensor_readings['acoustic'] >= 0 else 'FAULTY'
            },
            'uptime': len(self.data_history),
            'last_maintenance': self.last_update
        }
    
    def update_camera_status(self):
        """Update camera status from camera module"""
        if self.has_camera and self.camera_module:
            self.camera_status = self.camera_module.status


class ClusterHead:
    """Cluster Head for Data Aggregation and Communication"""
    
    def __init__(self, node_id, x, y, config):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.config = config
        self.is_active = True
        self.battery = 100.0  # Cluster heads typically have better power
        self.cluster_members = []  # List of sensor nodes in this cluster
        self.prediction_history = []
        self.data_buffer = []
        
        # Communication parameters
        self.communication_range = config["network"]["communication_range"]
        self.last_transmission = datetime.now()
        
    def add_cluster_member(self, sensor_node):
        """Add a sensor node to this cluster"""
        if sensor_node not in self.cluster_members:
            self.cluster_members.append(sensor_node)
            sensor_node.cluster_head_id = self.node_id
    
    def collect_cluster_data(self, all_sensor_nodes):
        """Collect and aggregate data from cluster members"""
        if not self.is_active:
            return None
        
        # Find active members in communication range
        active_members = []
        for node in all_sensor_nodes:
            if (node.is_active and 
                node.cluster_head_id == self.node_id and
                self._is_in_range(node)):
                active_members.append(node)
        
        if not active_members:
            return None
        
        # Aggregate sensor data
        sensor_summary = self._aggregate_sensor_data(active_members)
        
        cluster_data = {
            'cluster_id': self.node_id,
            'cluster_position': (self.x, self.y),
            'total_nodes': len(active_members),
            'active_members': [node.node_id for node in active_members],
            'sensor_summary': sensor_summary,
            'timestamp': datetime.now(),
            'battery_levels': [node.battery for node in active_members],
            'avg_signal_strength': np.mean([node.sensor_readings['signal_strength'] for node in active_members])
        }
        
        self.data_buffer.append(cluster_data)
        return cluster_data
    
    def _is_in_range(self, sensor_node):
        """Check if sensor node is within communication range"""
        distance = np.sqrt((self.x - sensor_node.x)**2 + (self.y - sensor_node.y)**2)
        return distance <= self.communication_range
    
    def _aggregate_sensor_data(self, active_members):
        """Aggregate sensor data from cluster members"""
        if not active_members:
            return {}
        
        # Collect all sensor readings
        pir_values = [node.sensor_readings['pir'] for node in active_members]
        vibration_values = [node.sensor_readings['vibration'] for node in active_members]
        thermal_values = [node.sensor_readings['thermal'] for node in active_members]
        acoustic_values = [node.sensor_readings['acoustic'] for node in active_members]
        
        # Collect the new extra data field (Max Temp Since Last Check)
        max_temp_values = [
            node.get_real_time_sensor_data()['sensors'].get('max_temp_since_last_check', 25.0) 
            for node in active_members
        ]
        
        # Calculate summary statistics
        sensor_summary = {
            'total_motion': sum(pir_values),
            'avg_vibration': np.mean(vibration_values),
            'max_vibration': np.max(vibration_values),
            'avg_temperature': np.mean(thermal_values),
            'max_temperature': np.max(max_temp_values), # <--- USING NEW AGGREGATED DATA
            'acoustic_events': sum(1 for val in acoustic_values if val > 0.5),
            'intrusion_nodes': sum(1 for node in active_members if node.sensor_readings['intrusion_detected']),
            'camera_nodes': sum(1 for node in active_members if node.has_camera and node.camera_status == "RECORDING")
        }
        
        return sensor_summary
    
    def update_prediction_history(self, prediction, confidence, timestamp):
        """Update prediction history for visualization"""
        prediction_entry = {
            'timestamp': timestamp,
            'prediction': prediction,
            'confidence': confidence
        }
        self.prediction_history.append(prediction_entry)
        
        # Keep only recent history
        if len(self.prediction_history) > 20:
            self.prediction_history.pop(0)
    
    def get_cluster_status(self):
        """Get cluster head status report"""
        return {
            'cluster_id': self.node_id,
            'position': (self.x, self.y),
            'active': self.is_active,
            'battery': self.battery,
            'member_count': len(self.cluster_members),
            'active_members': sum(1 for node in self.cluster_members if node.is_active),
            'last_transmission': self.last_transmission,
            'recent_predictions': len(self.prediction_history)
        }
    
    def simulate_energy_consumption(self):
        """Simulate energy consumption for cluster head"""
        # Base consumption
        consumption = 0.05
        
        # Additional consumption based on activity
        if self.data_buffer:
            consumption += 0.02 * len(self.data_buffer)
        
        self.battery = max(0, self.battery - consumption)
        
        # Deactivate if battery too low
        if self.battery < 5:
            self.is_active = False
            print(f"⚠️ Cluster Head {self.node_id} deactivated due to low battery")
