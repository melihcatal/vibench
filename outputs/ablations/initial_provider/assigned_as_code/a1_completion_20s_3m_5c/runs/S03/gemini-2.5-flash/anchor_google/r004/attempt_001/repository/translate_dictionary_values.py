from google.cloud import translate_v3


def translate_dictionary_values(payload, config=None):
    config = config or {}
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    translated_dict = {}
    for key, value in payload["dictionary"].items():
        response = client.translate_text(request={
            "parent": parent,
            "contents": [value],
            "mime_type": "text/plain",
            "source_language_code": payload["source_language"],
            "target_language_code": payload["target_language"],
        })
        translated_dict[key] = response.translations[0].translated_text
    return {
        "translated_dictionary": translated_dict,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
