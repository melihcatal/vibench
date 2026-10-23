import boto3

from translation_models import normalize_markup_payload


def translate_markup(payload, config=None):
    payload = normalize_markup_payload(payload)
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    response = client.translate_text(
        Text=payload["markup"],
        SourceLanguageCode=payload["source_language"],
        TargetLanguageCode=payload["target_language"],
        Settings={"Formality": "FORMAL"},
    )
    return {
        "markup": response["TranslatedText"],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
