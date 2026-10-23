from typing import Dict, List
import os
from google.cloud import language_v1
from translation_models import TranslationResponse


def summarize_quality_issues(
    translations: List[TranslationResponse],
) -> Dict[str, List[str]]:
    client = language_v1.LanguageServiceClient()
    issues = {"sentiment_issues": [], "syntax_issues": [], "entity_issues": []}

    for translation in translations:
        if isinstance(translation.translated_text, str):
            document = language_v1.Document(
                content=translation.translated_text,
                type_=language_v1.Document.Type.PLAIN_TEXT,
            )
            response = client.analyze_sentiment(request={"document": document})
            if response.document_sentiment.score < -0.5:
                issues["sentiment_issues"].append(translation.translated_text)

            response = client.analyze_syntax(request={"document": document})
            if len(response.tokens) > 20:
                issues["syntax_issues"].append(translation.translated_text)

            response = client.analyze_entities(request={"document": document})
            if len(response.entities) > 5:
                issues["entity_issues"].append(translation.translated_text)

    return issues
