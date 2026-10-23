import json
from google.cloud import aiplatform
from observability_client import resolve_log_source


def main() -> dict:
    model_name = "textembedding-gecko@003"
    client = aiplatform.gapic.PredictionServiceClient()
    return {"provider": "vertex-ai", "model": model_name, "source": resolve_log_source('embedding'), "client": client.__class__.__name__}


if __name__ == "__main__":
    print(json.dumps(main()))
