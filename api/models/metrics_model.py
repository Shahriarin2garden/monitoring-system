from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram
import time

class MetricsModel:
    def __init__(self):
        self.registry = CollectorRegistry()

        # Request metrics
        self.http_requests_total = Counter(
            "http_requests_total",
            "Total HTTP requests",
            labelnames=["method", "route", "status"],
            registry=self.registry
        )

        self.http_request_duration_seconds = Histogram(
            "http_request_duration_seconds",
            "HTTP request latency in seconds",
            labelnames=["method", "route"],
            buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
            registry=self.registry
        )

        self.http_requests_in_progress = Gauge(
            "http_requests_in_progress",
            "Active HTTP requests",
            labelnames=["method", "route"],
            registry=self.registry
        )

        # Error metrics
        self.api_errors_total = Counter(
            "api_errors_total",
            "Total API errors",
            labelnames=["error_type"],
            registry=self.registry
        )

        # Legacy metrics for backward compatibility
        self.request_count = Counter(
            "app_requests_total",
            "Total API requests",
            registry=self.registry
        )

        self.active_users = Gauge(
            "app_active_users",
            "Active users online",
            registry=self.registry
        )

        self.cpu_usage = Gauge(
            "app_cpu_usage_percent",
            "Simulated CPU usage",
            registry=self.registry
        )

    def record_request(self, method, route, status, duration):
        """Record HTTP request metrics"""
        try:
            self.http_requests_total.labels(method=method, route=route, status=str(status)).inc()
            self.http_request_duration_seconds.labels(method=method, route=route).observe(duration)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Error recording request metrics: {e}")

    def increment_in_progress(self, method, route):
        """Increment in-progress requests"""
        try:
            self.http_requests_in_progress.labels(method=method, route=route).inc()
        except Exception as e:
            print(f"Error incrementing in-progress metrics: {e}")

    def decrement_in_progress(self, method, route):
        """Decrement in-progress requests"""
        try:
            self.http_requests_in_progress.labels(method=method, route=route).dec()
        except Exception as e:
            print(f"Error decrementing in-progress metrics: {e}")

    def record_error(self, error_type):
        """Record API error"""
        try:
            self.api_errors_total.labels(error_type=error_type).inc()
        except Exception as e:
            print(f"Error recording error metrics: {e}")

    def update_users(self, users: int):
        try:
            self.request_count.inc()
            self.active_users.set(users)
        except Exception as e:
            print(f"Error updating user metrics: {e}")

    def update_cpu(self, value: float):
        try:
            self.cpu_usage.set(value)
        except Exception as e:
            print(f"Error updating CPU metrics: {e}")
