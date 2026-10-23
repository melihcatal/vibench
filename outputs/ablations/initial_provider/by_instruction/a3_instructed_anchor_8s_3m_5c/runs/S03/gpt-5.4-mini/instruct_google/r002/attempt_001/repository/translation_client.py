import os
from functools import lru_cache

from google.cloud import translate_v2 as translate


@lru_cache(maxsize=1)
def get_translation_client():
    return translate.Client()


def get_default_source_language() -> str:
    return os.getenv("TRANSLATION_SOURCE_LANGUAGE", "auto")


def get_default_target_language() -> str:
    return os.getenv("TRANSLATION_TARGET_LANGUAGE", "en")


def get_project_id() -> str:
    return os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCLOUD_PROJECT", ""))
