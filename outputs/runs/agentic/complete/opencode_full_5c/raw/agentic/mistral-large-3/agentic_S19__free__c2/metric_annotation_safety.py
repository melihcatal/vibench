import re
from typing import Dict, List
from google.cloud import language_v1


def check_metric_annotations(annotations: List[str]) -> Dict[str, List[str]]:
    client = language_v1.LanguageServiceClient()
    unsafe_annotations = {}

    for annotation in annotations:
        document = language_v1.Document(
            content=annotation, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_sentiment(request={"document": document})

        if response.document_sentiment.score < -0.5:
            unsafe_annotations.setdefault("negative_sentiment", []).append(annotation)

        response = client.moderate_text(request={"document": document})
        if response.moderation_categories:
            for category in response.moderation_categories:
                if category.confidence > 0.8:
                    unsafe_annotations.setdefault(category.name.lower(), []).append(
                        annotation
                    )

    return unsafe_annotations
