# Monitoring System

A complete monitoring stack with REST API, Prometheus scraping, and Grafana dashboards.

## Architecture

- **API**: FastAPI service that exposes Prometheus metrics
- **Prometheus**: Time-series database that scrapes metrics from the API
- **Grafana**: Visualization dashboard for monitoring

## Quick Start

### Prerequisites
- Docker
- Docker Compose

### Run the Stack

```bash
docker-compose up -d
```

This will start all three services:
- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default user: admin/admin)

## Workflow

### 1. Update Metrics

Update active users count via the API:

```bash
curl http://localhost:8000/update?users=12
```

### 2. View Raw Metrics

Access the metrics endpoint directly:

```bash
curl http://localhost:8000/metrics
```

### 3. Check Prometheus

Visit http://localhost:9090 to see scraped metrics

### 4. View Dashboards

Visit http://localhost:3000 and log in with `admin/admin`

## Available Metrics

- `app_requests_total`: Total number of requests (Counter)
- `app_active_users`: Current active users (Gauge)

## File Structure

```
monitoring-system/
├── api/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── prometheus/
│   ├── prometheus.yml
│   └── Dockerfile
├── grafana/
│   ├── provisioning/
│   │   ├── dashboards/
│   │   │   └── main-dashboard.json
│   │   └── datasources/
│   │       └── datasource.yml
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Stopping the Stack

```bash
docker-compose down
```
