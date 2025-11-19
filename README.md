AI-Enabled Intrusion Detection System using Wireless Sensor Networks (WSN)

This project simulates an intelligent Wireless Sensor Network (WSN)-based Intrusion Detection System powered by Artificial Intelligence.
It monitors a virtual border environment using 32 sensor nodes, 4 cluster heads, 8 simulated cameras, and an AI Gateway.

The system identifies Human, Animal, Vehicle, and Normal activities using a Random Forest Machine Learning model and triggers real-time alerts, camera verification, and dashboard visualization.

📌 Key Features
✅ 1. Wireless Sensor Network Simulation

32 virtual sensor nodes

Simulated PIR, vibration, acoustic, and temperature readings

Battery consumption + auto-recharge logic

Random but realistic sensor data generation

✅ 2. Cluster Head Architecture

4 cluster heads

Each CH aggregates readings from 8 sensors

Reduces communication load

Mimics real WSN energy-saving design

✅ 3. AI Gateway – Random Forest Classifier

Classifies intrusion as:

Human

Animal

Vehicle

Normal

Achieved 99.3% classification accuracy

Chosen because Random Forest performs best for tabular structured sensor data

Why Not SVM or Deep Learning?
Model	Reason Not Used
SVM	Slow for large number of features & cycles
Deep Learning	Needs huge dataset + GPU; not suitable for lightweight WSN simulation
Random Forest = Best for WSN

Handles noise

Runs fast

High accuracy

Works great with mixed sensor values

📌 System Architecture
The project works through 5 main stages:
1. Data Generation (models.py)

Simulates sensor behaviour such as motion, vibration, temperature, acoustic, battery level.

2. Data Aggregation (Cluster Heads)

Cluster heads compute meaningful features from raw sensor data.

3. AI Classification (ai_model.py)

Random Forest model predicts the intrusion type.

4. Camera Verification (camera_module.py)

Simulated camera checks the presence of human/animal/vehicle.

5. Real-time Alerts + Dashboard (visualization.py, notifications.py)

Shows intruder location, AI accuracy, and generates alerts.

📌 Files Explained
File	Purpose
main.py	The main program that runs every cycle
models.py	SensorNode + ClusterHead classes
config.py	Contains adjustable parameters
ai_model.py	Random Forest model logic
camera_module.py	Camera verification functions
notifications.py	Alert and logging system
visualization.py	Real-time dashboard
requirements.txt	Python dependencies
📌 How to Run
1. Install dependencies
pip install -r requirements.txt

2. Run the simulation
python main.py

📌 Future Enhancements

Multi-zone border simulation

Use of LoRa or Wi-Fi hardware sensors

Real-time GPS map

Drone-assisted surveillance

Live YOLO camera model
