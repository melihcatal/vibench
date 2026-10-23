from google.cloud import aiplatform_v1


def ocr_embedding(payload, config=None):
    config = config or {}
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = client.endpoint_path(config["project_id"], config["location"], config["endpoint_id"])
    instances = [{"content": section["text"]} for section in payload["sections"]]
    response = client.predict(endpoint=endpoint, instances=instances)
    return {"embeddings": [pred.prediction for pred in response.predictions]}
