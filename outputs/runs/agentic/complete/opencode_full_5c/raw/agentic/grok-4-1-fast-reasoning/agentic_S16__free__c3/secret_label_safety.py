import openai
import json
from typing import Dict, Any
from security_client import get_openai_key
from security_models import SafetyReport


def check_secret_label_safety(labels: Dict[str, str], notes: str) -> SafetyReport:
    key = get_openai_key()
    client = openai.OpenAI(api_key=key)
    text = notes + "\\nLabels: " + json.dumps(labels)
    response = client.moderations.create(input=text)
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories}
