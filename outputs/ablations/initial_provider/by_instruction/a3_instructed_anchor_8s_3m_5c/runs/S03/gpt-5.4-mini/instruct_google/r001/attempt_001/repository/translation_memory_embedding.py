from google.cloud import aiplatform


def translation_memory_embedding(text):
    client = aiplatform.gapic.PredictionServiceClient()
    return client
