# Sensor Data Analysis System

This project implements a comprehensive system for sensor data analysis, forecasting, and anomaly detection using a microservices architecture. The system processes telemetry data in real-time, provides predictions, and notifies users about anomalies through a web interface.

## System Architecture

The system consists of several components:

- Infrastructure services (Docker containers)
- Python-based analysis modules
- React-based web application
- Data processing and ML pipeline

## Prerequisites

- Docker and Docker Compose
- Python 3.x
- Node.js and npm

## Installation and Setup

### 1. Infrastructure Setup

Start all infrastructure components using Docker Compose:

```bash
docker compose up -d
```

This command will initialize:
- Apache Kafka and Zookeeper
- PostgreSQL database
- Kafka UI for monitoring
- pgAdmin for database management

### 2. Dependencies Installation

Install Python dependencies:
```bash
pip install -r src/requirements.txt
```

Install frontend dependencies:
```bash
cd src/sensor-data-web-app
npm install
```

### 3. Database Initialization

Set up the database schema:
```bash
python src/db_setup/init_db.py
```

### 4. Starting System Components

Launch the core processing modules (run each command in a separate terminal):

```bash
python src/sensor-data-analyzer/main.py
python src/sensor-data-forecaster/main.py
python src/sensor-data-notifier/main.py
```

### 5. Starting the Web Application

Launch the frontend application:
```bash
cd src/sensor-data-web-app
npm run start
```

### 6. Testing with Sample Data

To test the system with sample telemetry data:
```bash
python src/sensor-data-sender/main.py --filename sensor_data_10k.csv
```

Available sample data files:
- `sensor_data_10k.csv` - 10,000 records
- `sensor_data_50k.csv` - 50,000 records
- `sensor_data_100k.csv` - 100,000 records
- `sensor_data_all_100k.csv` - Complete dataset with approximatly 100,000 records

The system behavior can be configured through `src/config.json`:
```json
{
  "kafka": {
    "bootstrap_servers": "localhost:9092",
    "topics": {
      "raw_sensor_data": "in",
      "forecast": "forecast",
      "metrics": "metrics"
    },
    "message_delay_seconds": 0.01
  },
  "postgresql": {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "database_name": "postgres"
  }
}
```

Key configuration options:
- `message_delay_seconds`: Controls the delay between sending each message (default: 0.01 seconds)
- Kafka topics for different data streams
- PostgreSQL connection parameters

## System Access

After successful startup:
- Web Application: http://localhost:3000
- Kafka UI: http://localhost:8080
- pgAdmin: http://localhost:5050

## Architecture Overview

The system uses:
- Apache Kafka for message queuing
- PostgreSQL for data storage
- React for the frontend interface
- Python for data processing and analysis
- Docker for containerization and deployment

## Notes

- Ensure all Docker containers are healthy before proceeding with the application startup
- The system is designed to process real-time sensor data but can also work with historical data for testing
- All components are containerized for consistent deployment across different environments 