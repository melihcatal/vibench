import json
from google.cloud import translate_v3 as translate
from observability_client import resolve_log_source


def main() -> dict:
    client = translate.TranslationServiceClient()
    parent = f"projects/{resolve_log_source('translate')}/locations/global"
    text = ["Support-visible log message"]
    return {"provider": "google-cloud-translate", "parent": parent, "translated": text, "client": client.__class__.__name__}


if __name__ == "__main__":
    print(json.dumps(main()))
