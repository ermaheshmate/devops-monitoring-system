from flask import Flask, jsonify, Response, request
import psutil
import platform
from prometheus_client import Counter, Gauge, generate_latest

app = Flask(__name__)

# ================================
# Prometheus Metrics
# ================================

request_count = Counter(
    "app_requests_total",
    "Total number of application requests"
)

request_status = Counter(
    "app_requests_by_status_total",
    "Total number of application requests by HTTP status",
    ["status"]
)

cpu_usage = Gauge(
    "system_cpu_usage_percent",
    "Current CPU usage percentage"
)

memory_usage = Gauge(
    "system_memory_usage_percent",
    "Current memory usage percentage"
)

disk_usage = Gauge(
    "system_disk_usage_percent",
    "Current disk usage percentage"
)


# ================================
# Automatic Request Monitoring
# ================================

@app.after_request
def record_request(response):
    # Don't count Prometheus scraping itself
    if request.path != "/metrics":
        request_count.inc()
        request_status.labels(
            status=str(response.status_code)
        ).inc()

    return response


# ================================
# Routes
# ================================

@app.route("/")
def home():
    return jsonify({
        "application": "DevOps Monitoring System",
        "status": "running",
        "message": "Monitoring API is working"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/system")
def system_info():
    return jsonify({
        "platform": platform.system(),
        "platform_version": platform.version(),
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "memory_usage_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage("/").percent
    })

@app.route("/test-error")
def test_error():
    return jsonify({
        "error": "This is a test server error"
    }), 500


@app.route("/metrics")
def metrics():
    cpu_usage.set(psutil.cpu_percent(interval=None))
    memory_usage.set(psutil.virtual_memory().percent)
    disk_usage.set(psutil.disk_usage("/").percent)

    return Response(
        generate_latest(),
        mimetype="text/plain"
    )


# ================================
# Application Start
# ================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
