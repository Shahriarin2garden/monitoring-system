# Monitoring System — Complete MVP

A production-ready, fully containerized monitoring system with a clean MVC architecture. Includes a FastAPI REST API exporting Prometheus metrics, auto-configured Grafana dashboards, and Docker Compose orchestration.

---

## Overview

### Core Features

✔ **REST API** with FastAPI and MVC architecture  
✔ **Prometheus-compatible** `/metrics` endpoint  
✔ **Prometheus scraper** on 5-second intervals  
✔ **Grafana** with auto-provisioned data source & dashboard  
✔ **Full Docker Compose** orchestration  
✔ **Production-ready** configuration and setup  

### Included Metrics

- `app_requests_total` — Counter of total API requests
- `app_active_users` — Gauge for active user count
- `app_cpu_usage_percent` — Gauge for simulated CPU usage

---

## Architecture

```
┌──────────────┐      ┌─────────────┐      ┌─────────────┐
│   FastAPI    │      │ Prometheus  │      │   Grafana   │
│    (8000)    │─────▶│    (9090)   │◀─────│   (3000)    │
│   MVC App    │ Push  │  Time-Series│ Pull │ Dashboards │
└──────────────┘      └─────────────┘      └─────────────┘
  • Models             • Scrapes API        • Visualizes
  • Controllers        • 5s interval        • Auto-config
  • Views              • Time-series DB     • Pre-built dash
```

---

## Project Structure

```
monitoring-system/
│
├── api/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   │
│   ├── models/
│   │   └── metrics_model.py
│   │
│   ├── controllers/
│   │   └── metrics_controller.py
│   │
│   └── views/
│       └── metrics_view.py
│
├── prometheus/
│   ├── prometheus.yml
│   └── Dockerfile
│
├── grafana/
│   ├── Dockerfile
│   └── provisioning/
│       ├── datasources/
│       │   └── datasource.yml
│       └── dashboards/
│           └── main-dashboard.json
│
├── docker-compose.yml
└── README.md
```

---

## Quick Start

### Prerequisites

- **Docker** 20.10+
- **Docker Compose** 1.29+

### Deploy

```bash
docker-compose up -d
```

All three services will start in the background:

| Service | URL | Purpose |
|---------|-----|---------|
| **API** | http://localhost:8000 | Update metrics, view `/metrics` endpoint |
| **Prometheus** | http://localhost:9090 | Scraping & querying metrics |
| **Grafana** | http://localhost:3000 | Dashboards & visualization |

**Grafana default credentials:** `admin` / `admin`

---

## Usage

### 1. Update Active Users

```bash
curl "http://localhost:8000/update?users=42"
```

Response:
```json
{"status": "ok"}
```

### 2. Update CPU Usage

```bash
curl "http://localhost:8000/cpu?value=65.5"
```

Response:
```json
{"status": "ok"}
```

### 3. View Raw Metrics

```bash
curl http://localhost:8000/metrics
```

Output (Prometheus text format):
```
# HELP app_requests_total Total API requests
# TYPE app_requests_total counter
app_requests_total 2.0

# HELP app_active_users Active users online
# TYPE app_active_users gauge
app_active_users 42.0

# HELP app_cpu_usage_percent Simulated CPU usage
# TYPE app_cpu_usage_percent gauge
app_cpu_usage_percent 65.5
```

### 4. Access Prometheus

Navigate to http://localhost:9090

- Query metrics using PromQL
- View scrape jobs and targets
- Check scrape status and history

### 5. Access Grafana

Navigate to http://localhost:3000

- Login with `admin/admin`
- View pre-built **Monitoring System Dashboard**
- Panels include:
  - Active Users (gauge)
  - CPU Usage (time-series graph)
  - Requests Per Second (rate calculation)
  - All Metrics (table view)

---

## API Endpoints

| Endpoint | Method | Query Param | Description |
|----------|--------|------------|-------------|
| `/update` | GET | `users` (int ≥ 0) | Update active user count |
| `/cpu` | GET | `value` (float 0–100) | Update CPU usage percentage |
| `/metrics` | GET | — | Prometheus metrics in text format |

### Error Handling

- **Invalid users count** → `400 Bad Request` — "Users cannot be negative"
- **Invalid CPU value** → `400 Bad Request` — "CPU must be 0–100"

---

## MVC Architecture

### Models (`api/models/metrics_model.py`)

Manages Prometheus metric objects:
- `CollectorRegistry` — Holds all metrics
- `Counter` — `app_requests_total`
- `Gauge` — `app_active_users`, `app_cpu_usage_percent`

### Controllers (`api/controllers/metrics_controller.py`)

Handles business logic:
- Validates input (non-negative users, CPU 0–100)
- Calls model update methods
- Returns standardized JSON responses

### Views (`api/views/metrics_view.py`)

Formats responses for external systems:
- Converts metrics to Prometheus text format
- Returns with correct `Content-Type` header

---

## Configuration

### Prometheus Scrape Configuration
**File:** `prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: "api"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["api:8000"]
```

- Scrapes every 5 seconds
- Expects metrics at `/metrics` endpoint
- Targets the API container via Docker network

### Grafana Data Source
**File:** `grafana/provisioning/datasources/datasource.yml`

Auto-provisioned Prometheus data source:
- URL: `http://prometheus:9090`
- Set as default data source
- No authentication required (internal network)

---

## Stopping & Cleanup

### Stop All Containers

```bash
docker-compose down
```

### Stop + Remove Volumes

```bash
docker-compose down -v
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f prometheus
docker-compose logs -f grafana
```

---

## Troubleshooting

### API Not Responding

```bash
docker-compose logs api
```

Check for import errors or Python dependency issues.

### Prometheus Can't Scrape API

Visit http://localhost:9090/targets — verify the API target status.

### Grafana Can't Connect to Prometheus

Check the data source configuration in Grafana settings (⚙️ → Data Sources).

### Rebuild Containers

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## Next Steps

- **Custom metrics**: Add new `Gauge` or `Counter` objects in `models/metrics_model.py`
- **Advanced dashboards**: Edit `grafana/provisioning/dashboards/main-dashboard.json`
- **Alerting**: Configure Prometheus alerting rules in `prometheus/prometheus.yml`
- **Production deployment**: Use environment variables, secrets management, and persistent volumes

---

## License

MIT
