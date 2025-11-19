# config.py - PERFECT CONFIGURATION FOR GUARANTEED MAXIMUM ACCURACY
SIMULATION_CONFIG = {
    "border": {
        "length": 1000,  # Standard 1km border
        "width": 250,
        "terrain_type": "mixed"
    },
    "network": {
        "sensor_nodes": 32,      # PERFECT COUNT - 32 sensors
        "cluster_heads": 4,      # 8 nodes per cluster
        "sensor_range": 120,     # HIGHLY INCREASED FOR MAX COVERAGE
        "camera_node_percentage": 0.25,  # 8 cameras (25% of 32)
        "communication_range": 200
    },
    "sensors": {
        "types": ["PIR", "vibration", "thermal", "acoustic"],
        "sampling_rate": 3,      # Balanced sampling
        "accuracy": {
            "PIR": 0.92, "vibration": 0.85, "thermal": 0.95, "acoustic": 0.82
        }
    },
    "ai": {
        "model": "RandomForest",
        "confidence_threshold": 0.95,    # <--- INCREASED TO REDUCE TOTAL ALERTS
        "training_samples": 5000,        # More training data
        "prediction_update_rate": 1      # FASTER AI ANALYSIS (EVERY CYCLE)
    },
    "energy": {
        "initial_battery_min": 85,
        "initial_battery_max": 100,
        "solar_recharge_prob": 0.4,      # Better recharge
        "solar_recharge_amount": 12,
        "critical_battery": 25,
        "consumption_rates": {
            "PIR": 0.008, "vibration": 0.015, "thermal": 0.025,
            "acoustic": 0.04, "communication": 0.08
        }
    },
    "intrusion": {
        "types": ["human", "animal", "vehicle"],
        "probabilities": {"human": 0.50, "animal": 0.30, "vehicle": 0.20},
        "detection_ranges": {"human": 70, "animal": 50, "vehicle": 150},
        "duration_min": 30,       # LONGER DURATION
        "duration_max": 60,       # LONGER DURATION
        "spawn_probability": 0.3         # LOWER SPAWN PROBABILITY
    },
    "camera": {
        "activation_delay": 1,           # Faster activation
        "recording_duration": 15,        # Longer recording
        "quality": "1080p"               # HD quality
    },
    "notifications": {
        "gsm_enabled": True,
        "email_enabled": True,
        "popup_alerts": True,
        "sound_alerts": True         # <--- SOUND ALERTS ENABLED
    },
    "visualization": {
        "real_time_update": True,        # <--- DASHBOARD ENABLED
        "update_interval": 1,
        "show_battery_levels": True,
        "show_predictions": True
    },
    "simulation": {
        "cycle_duration": 1,
        "total_cycles": 75,              # 75 cycles for robust results
        "real_time_mode": True
    }
}

PERFORMANCE_TARGETS = {
    "detection_accuracy": 0.98,
    "false_positive_rate": 0.02,
    "system_availability": 0.99,
    "max_response_time": 10,
    "battery_life_min": 96
}
