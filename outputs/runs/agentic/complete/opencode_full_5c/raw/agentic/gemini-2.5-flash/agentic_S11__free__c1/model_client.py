from google.cloud import aiplatform


def get_prediction_client():
    return aiplatform.PredictionServiceClient()
