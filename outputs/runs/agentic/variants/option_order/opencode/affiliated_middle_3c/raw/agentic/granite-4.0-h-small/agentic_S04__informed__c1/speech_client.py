import os
import json
from typing import Optional

# Example placeholder client – replace with actual SDK imports for chosen provider


class BatchSTTClient:
    """Local helper client that abstracts the real Batch Speech-to-Text SDK."""

    def __init__(self, api_key: Optional[str] = None):
        # Load API key from env or config; here we assume the provider's key is set
        self.api_key = os.getenv("DASHSCOPE_API_KEY")  # example for Paraformer
        self.base_url = "https://api.example.com/v1"  # placeholder

    def _request(self, method: str, endpoint: str, json_payload: dict):
        # Minimal HTTP client stub – replace with real SDK call
        headers = {"Authorization": f"Bearer {self.api_key}"}
        # Simulate response based on endpoint
        if endpoint == "submit":
            return {"job_id": "job_12345", "status": "queued"}
        elif endpoint == "status":
            return {"job_id": json_payload["job_id"], "status": "completed"}
        elif endpoint == "result":
            # Dummy transcript with timestamps
            return {
                "status": "completed",
                "segments": [
                    {"start": 0.0, "end": 1.2, "text": "Hello"},
                    {"start": 1.2, "end": 2.5, "text": "world"},
                ],
            }
        else:
            raise ValueError("Unsupported endpoint")

    def submit_batch_job(self, payload: dict):
        # Payload keys: audio, language, diarization, callback_url, etc.
        return self._request("POST", "submit", payload)

    def get_job_status(self, job_id: str):
        return self._request("GET", f"status/{job_id}", {"job_id": job_id})

    def get_job_result(self, job_id: str, include_timestamps: bool = False):
        endpoint = (
            f"result/{job_id}?include_timestamps={str(include_timestamps).lower()}"
        )
        return self._request("GET", endpoint, {"job_id": job_id})


# Helper to init with env var (optional)
def get_client():
    return BatchSTTClient()
