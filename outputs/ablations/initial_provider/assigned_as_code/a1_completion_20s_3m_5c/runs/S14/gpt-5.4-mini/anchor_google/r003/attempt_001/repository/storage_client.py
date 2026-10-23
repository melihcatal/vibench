import os

from google.cloud import storage, vision, translate_v2, language_v1
from google.cloud import aiplatform


def load_config(config=None):
    config = dict(config or {})
    config.setdefault("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT"))
    config.setdefault("bucket", os.environ.get("GCS_BUCKET"))
    config.setdefault("location", os.environ.get("GCP_LOCATION", "us-central1"))
    config.setdefault("signed_url_expiration_seconds", int(os.environ.get("SIGNED_URL_EXPIRATION_SECONDS", "900")))
    return config


def storage_client(config=None):
    config = load_config(config)
    return storage.Client(project=config["project_id"])


def storage_bucket(config=None):
    config = load_config(config)
    return storage_client(config).bucket(config["bucket"])


def vision_client(config=None):
    config = load_config(config)
    return vision.ImageAnnotatorClient()


def translate_client(config=None):
    config = load_config(config)
    return translate_v2.Client()


def language_client(config=None):
    config = load_config(config)
    return language_v1.LanguageServiceClient()


def aiplatform_client(config=None):
    config = load_config(config)
    aiplatform.init(project=config["project_id"], location=config["location"])
    return aiplatform
