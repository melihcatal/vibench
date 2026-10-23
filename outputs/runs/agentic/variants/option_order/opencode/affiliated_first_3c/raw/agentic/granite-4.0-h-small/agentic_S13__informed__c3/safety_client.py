# [HELPER] safety_client.py

import os
from typing import Any, Dict, List, Optional

# Choose a concrete provider (watsonx guardrails) for the safety layer.
# The class encapsulates configuration, client creation, and a simple `analyze`
# method that returns a dict compatible with the SAME-scenario files.


class TextSafetyClient:
    """Local wrapper around a concrete Text Content Safety provider.

    This implementation uses the watsonx guardrails service as the concrete
    provider.  It reads configuration from environment variables and provides
    a unified API (`analyze`) used by the scored files.
    """

    def __init__(self):
        # Provider credentials (example: watsonx)
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        if not self.api_key or not self.project_id:
            raise RuntimeError(
                "Environment variables WATSONX_API_KEY and WATSONX_PROJECT_ID must be set"
            )
        # Instantiate provider SDK client (sdk_or_rest interface)
        from ibm_watsonx_ai import APIClient

        self.client = APIClient(api_key=self.api_key, project_id=self.project_id)

    def analyze(self, text: str) -> Dict[str, Any]:
        """Send `text` to the safety service and return a normalized response dict.

        The structure matches what the SAME-scenario files expect:
        {
            'unsafe': bool,
            'categories': List[Dict[str, str]],  # e.g., [{'name':'hate','severity':1}, ...]
        }
        """
        # Example SDK call; adjust to the actual guardrails endpoint you use.
        from ibm_watsonx_ai.hlp.detection import HapDetection

        response = HapDetection.detect(self.client, text)
        # Normalize to our simple schema
        result: Dict[str, Any] = {"unsafe": False, "categories": []}
        if response.get("unsafe"):
            result["unsafe"] = True
            # Convert provider categories to our format
            for cat in response.get("categories", []):
                result["categories"].append(
                    {"name": cat["category_name"], "severity": cat["severity_level"]}
                )
        return result
