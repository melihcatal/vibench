import os
from typing import List, Dict, Any
from google.cloud import language_v2

def check_corpus_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """Checks corpus text for safety using Google Cloud's Language API.

    Args:
        texts: A list of text strings to check.

    Returns:
        A list of dictionaries, each containing the original text and its safety assessment.
    """
    client = language_v2.LanguageServiceClient()
    safety_results = []

    for text_content in texts:
        document = language_v2.Document(content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT)
        response = client.moderate_text(document=document)
        
        # Extract relevant safety attributes. The exact structure might vary slightly by API version.
        # This is a simplified representation.
        categories_info = []
        for category_filter in response.safety_attributes.categories:
            categories_info.append({
                "category": category_filter.category,
                "violence": category_filter.violence,
                "derogatory": category_filter.derogatory,
                "sexual": category_filter.sexual,
                "medical": category_filter.medical,
                "health": category_filter.health,
                "harmful_content": category_filter.harmful_content,
            })

        safety_results.append({
            "text": text_content,
            "safety_attributes": categories_info
        })
    return safety_results

