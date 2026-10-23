import os
import requests
import json
from database_models import Document
from typing import Dict


def check_record_safety(record: Document) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    text = record.get("content", "") or record.get("title", "") or str(record)
    data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(
        url,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        params={"key": api_key},
    )
    result = response.json()
    toxicity = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {"toxicity_score": toxicity, "is_safe": toxicity < 0.5}
