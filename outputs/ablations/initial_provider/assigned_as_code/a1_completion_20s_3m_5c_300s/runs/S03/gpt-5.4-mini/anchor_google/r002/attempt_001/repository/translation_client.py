import os

from google.cloud import translate_v3


def load_translation_config(config=None):
    config = dict(config or {})
    config.setdefault("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT"))
    config.setdefault("location", os.environ.get("GOOGLE_CLOUD_LOCATION", "global"))
    return config


def get_translation_client():
    return translate_v3.TranslationServiceClient()


def build_translation_parent(config):
    return f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
