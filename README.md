# DevOps Monitoring System

A hands-on Docker Compose monitoring stack demonstrating Flask application metrics collection, Prometheus scraping, and Grafana visualization.

## Stack
- Flask (Python) application with health/system/metrics endpoints
- Prometheus for metrics scraping
- Grafana for dashboards
- Docker Compose for orchestration

## Endpoints
- `/` — application status
- `/health` — health check (`{"status":"healthy"}`)
- `/system` — CPU, disk, memory, platform info
- `/metrics` — Prometheus-formatted metrics

## Running locally
```bash
docker compose up -d
```

- App: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Status
Actively developed as part of a hands-on DevOps learning project.
