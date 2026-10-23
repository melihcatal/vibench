import boto3

from translation_client import get_translate_client
from translation_models import TranslationResponse


def translation_memory_embedding(texts, source_language, target_language, config=None):
    client = get_translate_client(config)
    responses = client.batch_translate_text(
        Requests=[
            {
                'Text': text,
                'SourceLanguageCode': source_language,
                'TargetLanguageCode': target_language,
            }
            for text in texts
        ]
    )
    embeddings = [
        TranslationResponse.from_dict(response).to_dict()['text']
        for response in responses['TranslatedTexts']
    ]
    return embeddings