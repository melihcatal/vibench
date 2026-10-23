from google.cloud import aiplatform_v1


def embed_script(text: str, endpoint: str) -> list[float]:
    client = aiplatform_v1.PredictionServiceClient()
    instances = [{"content": text}]
    response = client.predict(endpoint=endpoint, instances=instances)
    predictions = response.predictions or []
    if predictions and isinstance(predictions[0], dict) and "embeddings" in predictions[0]:
        return list(predictions[0]["embeddings"])
    if predictions and isinstance(predictions[0], dict) and "values" in predictions[0]:
        return list(predictions[0]["values"])
    return []
