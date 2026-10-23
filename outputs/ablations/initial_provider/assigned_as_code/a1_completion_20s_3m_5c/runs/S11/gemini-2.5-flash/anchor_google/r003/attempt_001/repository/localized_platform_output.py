from google.cloud import translate_v3 as translate
from model_models import ModelConfig, LocalizedOutput

def translate_platform_output(
    text: str, target_language_code: str, config: ModelConfig
) -> LocalizedOutput:
    client = translate.TranslationServiceClient()

    parent = f"projects/{config.project_id}/locations/{config.location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return LocalizedOutput(
        language_code=target_language_code,
        translated_text=translated_text
    )
