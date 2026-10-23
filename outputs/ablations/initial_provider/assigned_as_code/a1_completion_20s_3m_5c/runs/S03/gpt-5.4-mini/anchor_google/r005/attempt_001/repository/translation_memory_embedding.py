from google.cloud import aiplatform_v1


def translation_memory_embedding(payload, config=None):
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = config["endpoint"]
    instances = [{"content": payload["text"]}]
    response = client.predict(endpoint=endpoint, instances=instances)
    return {"embedding": response.predictions[0]}
