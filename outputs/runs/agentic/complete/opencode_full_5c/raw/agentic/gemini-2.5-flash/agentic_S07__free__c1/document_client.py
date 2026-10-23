from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import os


def get_document_ai_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    # You can specify a regional endpoint
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    return documentai.DocumentProcessorServiceClient(client_options=client_options)


def get_translation_client():
    from google.cloud import translate_v3

    return translate_v3.TranslationServiceClient()


def get_vertex_ai_prediction_client():
    from google.cloud import aiplatform

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get(
        "GOOGLE_CLOUD_LOCATION", "us-central1"
    )  # Vertex AI often uses us-central1
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )
