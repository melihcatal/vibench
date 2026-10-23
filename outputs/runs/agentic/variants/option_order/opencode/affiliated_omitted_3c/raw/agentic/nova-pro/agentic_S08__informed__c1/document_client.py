import os


def get_document_client():
    return {
        "mindee_api_key": os.getenv("MINDEE_API_KEY"),
        "google_application_credentials": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    }
