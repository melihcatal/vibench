import os

from google.cloud import translate_v3


def get_config(config=None):
    merged = dict(config or {})
    if "project_id" not in merged:
        merged["project_id"] = os.environ["GOOGLE_CLOUD_PROJECT"]
    merged.setdefault("location", os.getenv("GOOGLE_CLOUD_LOCATION", "global"))
    return merged


def get_translation_client(config=None):
    config = get_config(config)
    return translate_v3.TranslationServiceClient()
