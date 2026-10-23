from observability_client import ObservabilityClient


def metric_annotation_safety(text: str):
    client = ObservabilityClient(endpoint="https://api.openai.com/v1")
    return client.post("/moderations", {"model": "omni-moderation-latest", "input": text})
