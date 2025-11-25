from prometheus_client import CollectorRegistry, Counter, Gauge

class MetricsModel:
    def __init__(self):
        self.registry = CollectorRegistry()

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

    def update_users(self, users: int):
        self.request_count.inc()
        self.active_users.set(users)

    def update_cpu(self, value: float):
        self.cpu_usage.set(value)
