from fastapi import Response
from prometheus_client import generate_latest

class MetricsView:

    @staticmethod
    def as_prometheus(registry):
        output = generate_latest(registry)
        return Response(output, media_type="text/plain")
