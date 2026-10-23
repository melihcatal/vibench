from google.cloud import monitoring_v3


class ObservabilityClient:
    def __init__(self, project_id: str = None):
        self.project_id = project_id or self._get_project_id()
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{self.project_id}"

    def _get_project_id(self) -> str:
        import os

        return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT_ID")

    def build_time_interval(self, hours: int = 1) -> dict:
        import datetime

        now = datetime.datetime.utcnow()
        start_time = now - datetime.timedelta(hours=hours)
        return {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
