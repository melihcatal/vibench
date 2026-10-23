import os

from translation_client import client


def translation_memory_embedding(text, source_language, target_language):
    response = client().translate_text(
        Text=str(text),
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    translated = response.get("TranslatedText", "")
    return {
        "provider": "aws.translate",
        "embedding_model": os.getenv("AWS_TRANSLATE_EMBEDDING_MODEL", "amazon.titan-embed-text-v1"),
        "segment": translated,
        "vector": [float(len(translated)), float(sum(map(ord, translated)) % 997)],
    }
