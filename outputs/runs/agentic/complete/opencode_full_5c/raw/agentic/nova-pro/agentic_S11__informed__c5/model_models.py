from google.cloud import aiplatform


class PredictionRequest:
    def __init__(self, instances):
        self.instances = instances


class PredictionResponse:
    def __init__(self, predictions):
        self.predictions = predictions


def normalize_response(response):
    return PredictionResponse(response.predictions)
