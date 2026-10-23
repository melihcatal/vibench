from google.cloud import language_v1
from typing import List, Dict, Any

def check_unsafe_copy(texts: List[str]) -> Dict[str, Any]:
    """Checks localized copy for potentially unsafe content using Google Cloud Natural Language's classify_text.

    This function attempts to categorize text to identify content that might be deemed unsafe
    or inappropriate based on Google's predefined content categories.

    Args:
        texts: A list of text segments to check.

    Returns:
        A dictionary summarizing potential unsafe content, categorized by detected categories.
    """
    client = language_v1.LanguageServiceClient()
    unsafe_content_report = {"potentially_unsafe_categories": {}}

    for i, text in enumerate(texts):
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.classify_text(request={'document': document})

        detected_categories = []
        for category in response.categories:
            # Cloud Natural Language API provides categories like /Adult, /Social Issues, etc.
            # We can flag certain categories as 'potentially unsafe'.
            if category.name.startswith('/Adult') or category.name.startswith('/Violence') or \
               category.name.startswith('/Discrimination') or category.name.startswith('/Hate Speech'):
                detected_categories.append({"name": category.name, "confidence": category.confidence})
        
        if detected_categories:
            unsafe_content_report["potentially_unsafe_categories"][f"text_segment_{i}"] = {
                "text": text,
                "categories": detected_categories
            }

    return unsafe_content_report
