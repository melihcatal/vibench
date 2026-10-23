import os
import json
import requests

class CloudLogsClient:
    """Simple wrapper for IBM Cloud Logs REST API."""
    BASE_URL = "https://api.us-south.logs.cloud.ibm.com"
    def __init__(self):
        self.api_key = os.getenv("IBM_CLOUD_API_KEY")
        self.instance_id = os.getenv("IBM_LOGS_INSTANCE_ID")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
    def now_iso(self) -> str:
        """Return current UTC timestamp in ISO 8601 format."""
        return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    def post(self, endpoint: str, json: dict) -> requests.Response:
        """Send a POST request to the logs endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        return requests.post(url, headers=self.headers, json=json)

# Helper to supply singleton client
_client = CloudLogsClient()
def get_client() -> CloudLogsClient:
    """Return the configured client (singleton)."""
    return _client
