import os
from typing import List, Dict
from google.cloud import language_v2  # Google Cloud Natural Language API


def check_corpus_safety(texts: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """Checks corpus text before embedding using Google Cloud Natural Language API for safety attributes.
    This function aims to identify potentially unsafe content based on Google's content moderation models.
    """
    client = language_v2.LanguageServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    document_gcs_content = []
    for text_content in texts:
        document_gcs_content.append(
            language_v2.Document(
                content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
            )
        )

    safety_results = []
    for doc_content in document_gcs_content:
        request = language_v2.AnalyzeSafetyAttributesRequest(
            document=doc_content,
        )
        response = client.analyze_safety_attributes(request=request)
        # Extract relevant safety attributes, e.g., categories and scores
        # For simplicity, we'll just store the raw response for each text
        safety_results.append(
            {
                "text": doc_content.content,
                "safety_attributes": [
                    {"category": score.category.name, "score": score.score}
                    for score in response.safety_attributes.categories
                ],
            }
        )

    return {"safety_checks": safety_results}
