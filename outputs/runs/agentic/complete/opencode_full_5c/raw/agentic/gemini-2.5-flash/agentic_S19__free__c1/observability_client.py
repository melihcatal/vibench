import os
from google.cloud import monitoring_v3
from google.cloud import translate_v3
from google.cloud import storage
from google.cloud import aiplatform


def get_monitoring_client():
    return monitoring_v3.MetricServiceClient()


def get_translate_client():
    return translate_v3.TranslationServiceClient()


def get_storage_client():
    return storage.Client()


def get_aiplatform_prediction_client(location: str):
    return aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )


def get_project_id():
    return os.environ.get("GCP_PROJECT_ID")
