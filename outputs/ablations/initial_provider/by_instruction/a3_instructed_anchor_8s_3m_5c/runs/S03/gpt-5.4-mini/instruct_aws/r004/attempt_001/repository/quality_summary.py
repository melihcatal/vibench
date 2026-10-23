import os

from translation_client import client


def quality_summary(text, source_language, target_language):
    response = client().translate_text(
        Text=str(text),
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
        Settings={"Brevity": "OFF"},
    )
    return {
        "provider": "aws.translate",
        "model": os.getenv("AWS_TRANSLATE_MODEL", "amazon-translate"),
        "translated_text": response.get("TranslatedText", ""),
        "issues": [item for item in response.get("AppliedSettings", {}).items()],
    }
