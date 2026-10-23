import os
from typing import Any, Dict

import deepl


def get_translation_config() -> Dict[str, Any]:
    return {
        "auth_key": os.environ.get("DEEPL_AUTH_KEY", ""),
        "use_free_api": os.environ.get("DEEPL_USE_FREE_API", "false").lower() == "true",
    }


def create_translation_client() -> deepl.Translator:
    config = get_translation_config()
    return deepl.Translator(config["auth_key"], use_free_api=config["use_free_api"])
