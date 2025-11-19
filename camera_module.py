 # camera_module.py - Enhanced with better integration and AUTO-RECOVERY
import random
import time
from datetime import datetime
import numpy as np

class CameraModule:
    """Real-time Camera Simulation Module with AUTO-RECOVERY"""
    
    def __init__(self, sensor_node):
        self.sensor_node = sensor_node
        self.camera_id = f"CAM_{sensor_node.node_id}"
        self.status = "IDLE"  # IDLE, RECORDING, PROCESSING, FAULTY
        self.recording_start = None
        self.footage_log = []
        self.detection_log = []
        
        # Camera specifications
        self.specs = {
            'resolution': '1280x720',
            'fps': 30,
            'zoom': '4x',
            'night_vision': True,
            'storage_capacity': 48,  # hours
            'motion_sensitivity': 0.7
        }
        
        # AI object detection capabilities
        self.detection_capabilities = ['human', 'vehicle', 'animal', 'suspicious_object']
        
        # Performance metrics
        self.performance_metrics = {
            'total_recordings': 0,
            'total_detections': 0,
            'average_confidence': 0.0,
            'uptime': 0
        }

    def activate_recording(self, trigger_reason="motion_detected", intrusion_type=None):
        """Activate camera recording with enhanced logic and TYPE-SPECIFIC DURATION"""
        if self.status != "FAULTY" and self.sensor_node.is_active:
            self.status = "RECORDING"
            self.recording_start = datetime.now()
            
            # Determine custom duration based on intrusion type (New Logic)
            if intrusion_type == 'vehicle':
                custom_duration = 30 # Record vehicle for 30s
            elif intrusion_type == 'human':
                custom_duration = 20 # Record human for 20s
            else:
                custom_duration = 15 # Default duration
            
            # Create footage entry
            footage = {
                'camera_id': self.camera_id,
                'start_time': self.recording_start,
                'trigger': trigger_reason,
                'expected_duration': custom_duration, # New field
                'duration': 0,
                'objects_detected': [],
                'footage_quality': self._assess_quality(),
                'file_size': random.uniform(50, 200),  # MB
                'sensor_data_snapshot': self.sensor_node.sensor_readings.copy()
            }
            
            self.footage_log.append(footage)
            self.performance_metrics['total_recordings'] += 1
            
            print(f"道 Camera {self.camera_id} started recording ({custom_duration}s) - {trigger_reason}")
            return True
        return False

    def stop_recording(self):
        """Stop camera recording with analytics"""
        if self.status == "RECORDING":
            self.status = "IDLE"
            duration = (datetime.now() - self.recording_start).total_seconds()
            
            # Update last footage entry
            if self.footage_log:
                self.footage_log[-1]['duration'] = duration
                self.footage_log[-1]['end_time'] = datetime.now()
                self.footage_log[-1]['final_quality'] = self._assess_quality()
            
            print(f"道 Camera {self.camera_id} stopped recording ({duration:.1f}s)")
            return duration
        return 0

    def process_live_feed(self):
        """Process live camera feed for object detection with enhanced logic"""
        # Only process if recording and sensor indicates intrusion
        if (self.status == "RECORDING" and 
            self.sensor_node.sensor_readings['intrusion_detected'] and
            random.random() < 0.6):  # 60% chance when intrusion detected
            
            detected_objects = self._simulate_object_detection()
            
            if detected_objects:
                detection_entry = {
                    'timestamp': datetime.now(),
                    'camera_id': self.camera_id,
                    'objects': detected_objects,
                    'confidence': random.uniform(0.7, 0.95),
                    'position_estimate': (self.sensor_node.x, self.sensor_node.y),
                    'sensor_correlation': {
                        'pir': self.sensor_node.sensor_readings['pir'],
                        'vibration': self.sensor_node.sensor_readings['vibration'],
                        'thermal': self.sensor_node.sensor_readings['thermal'],
                        'acoustic': self.sensor_node.sensor_readings['acoustic']
                    }
                }
                
                self.detection_log.append(detection_entry)
                self.performance_metrics['total_detections'] += 1
                
                # Update performance metrics
                confidences = [obj['confidence'] for obj in detected_objects]
                self.performance_metrics['average_confidence'] = np.mean(confidences)
                
                # Update footage log
                if self.footage_log:
                    self.footage_log[-1]['objects_detected'].extend(detected_objects)
                
                print(f"識 Camera {self.camera_id} detected {len(detected_objects)} objects")
                return detection_entry
        
        return None

    def _simulate_object_detection(self):
        """Simulate AI object detection in camera feed with enhanced logic"""
        detected_objects = []
        
        # Use sensor readings to influence detection
        readings = self.sensor_node.sensor_readings
        
        # Base detection probability on sensor confidence
        detection_confidence = min(1.0, (
            readings['pir'] + 
            readings['vibration'] * 0.8 +
            (readings['thermal'] - 25) / 20 * 0.5 +
            readings['acoustic'] * 0.7
        ))
        
        if detection_confidence > 0.3:  # Minimum threshold
            intrusion_type = self._infer_intrusion_type()
            
            if intrusion_type:
                detected_objects.append({
                    'type': intrusion_type,
                    'confidence': max(0.5, detection_confidence + random.uniform(-0.2, 0.1)),
                    'size': random.uniform(0.1, 1.0),
                    'movement': random.choice(['stationary', 'slow', 'fast']),
                    'distance_estimate': random.uniform(5, 50),  # meters
                    'bounding_box': {
                        'x': random.uniform(0.1, 0.9),
                        'y': random.uniform(0.1, 0.9),
                        'width': random.uniform(0.1, 0.3),
                        'height': random.uniform(0.1, 0.3)
                    }
                })
        
        return detected_objects

    def _infer_intrusion_type(self):
        """Infer intrusion type from sensor patterns with enhanced logic"""
        readings = self.sensor_node.sensor_readings
        
        # Multi-sensor fusion for better classification
        vibration_score = readings['vibration']
        thermal_score = (readings['thermal'] - 25) / 15  # Normalized
        acoustic_score = readings['acoustic']
        
        if vibration_score > 0.7 and thermal_score > 0.5:
            return 'vehicle'
        elif thermal_score > 0.6 and vibration_score < 0.4:
            return 'human'
        elif 0.3 < vibration_score < 0.6 and thermal_score < 0.5:
            return 'animal'
        elif acoustic_score > 0.8:
            return 'suspicious_object'
        else:
            return 'unknown'

    def _assess_quality(self):
        """Assess footage quality based on conditions with enhanced factors"""
        quality_factors = {
            'battery_impact': max(0, 1 - (100 - self.sensor_node.battery) / 100),
            'signal_impact': self.sensor_node.sensor_readings['signal_strength'],
            'environment_impact': random.uniform(0.7, 1.0),
            'time_impact': 0.8 if 6 <= datetime.now().hour <= 18 else 0.5  # Day/Night
        }
        
        overall_quality = np.mean(list(quality_factors.values()))
        
        if overall_quality > 0.8:
            return "EXCELLENT"
        elif overall_quality > 0.6:
            return "GOOD"
        elif overall_quality > 0.4:
            return "FAIR"
        else:
            return "POOR"

    def get_camera_status(self):
        """Get comprehensive camera status with enhanced metrics"""
        return {
            'camera_id': self.camera_id,
            'status': self.status,
            'parent_node': self.sensor_node.node_id,
            'position': (self.sensor_node.x, self.sensor_node.y),
            'battery': self.sensor_node.battery,
            'specifications': self.specs,
            'recording_duration': len(self.footage_log),
            'detections_made': len(self.detection_log),
            'storage_used': sum(f['file_size'] for f in self.footage_log),
            'health': self._get_camera_health(),
            'performance': self.performance_metrics,
            'current_quality': self._assess_quality() if self.status == "RECORDING" else "N/A"
        }

    def _get_camera_health(self):
        """Assess camera health with enhanced criteria"""
        if self.sensor_node.battery < 10 or self.status == "FAULTY":
            return "CRITICAL"
        elif self.sensor_node.battery < 30:
            return "LOW"
        elif len(self.footage_log) > 100:  # High usage
            return "MODERATE"
        else:
            return "GOOD"

    def simulate_camera_fault(self, fault_type=None):
        """Simulate camera faults for testing with enhanced logic"""
        if fault_type == "random" and random.random() < 0.005:  # REDUCED to 0.5% chance
            self.status = "FAULTY"
            print(f"肌 Camera {self.camera_id} fault simulated")
            
        elif fault_type == "battery_low" and self.sensor_node.battery < 15:
            self.status = "FAULTY"
            print(f"萩 Camera {self.camera_id} fault due to low battery")

    def attempt_auto_recovery(self):
        """ATTEMPT AUTO-RECOVERY FROM CAMERA FAULTS - NEW METHOD"""
        if self.status == "FAULTY" and random.random() < 0.1:  # 10% recovery chance
            self.status = "IDLE"
            print(f"肌 Camera {self.camera_id} automatically recovered from fault")
            return True
        return False

    def get_recent_detections(self, count=5):
        """Get recent object detections with enhanced info"""
        recent = self.detection_log[-count:] if self.detection_log else []
        for detection in recent:
            detection['quality_assessment'] = self._assess_quality()
        return recent

    def get_storage_info(self):
        """Get camera storage information with enhanced metrics"""
        total_size = sum(f['file_size'] for f in self.footage_log)
        capacity = self.specs['storage_capacity'] * 1024  # Convert hours to MB approx
        
        return {
            'used_mb': round(total_size, 2),
            'available_mb': max(0, capacity - total_size),
            'usage_percent': (total_size / capacity) * 100 if capacity > 0 else 0,
            'footage_count': len(self.footage_log),
            'average_file_size': total_size / len(self.footage_log) if self.footage_log else 0,
            'estimated_remaining_hours': (capacity - total_size) / (125 * 24)  # Approx hours
        }
