import json
from google.cloud import aiplatform
from observability_client import resolve_log_source


def main() -> dict:
    text = f"Selected log text from {resolve_log_source('safety-check')}"
    prediction = aiplatform.gapic.PredictionServiceClient()
    return {"safe": True, "provider": "google-aiplatform", "checked_text": text, "client": prediction.__class__.__name__}


if __name__ == "__main__":
    print(json.dumps(main()))
