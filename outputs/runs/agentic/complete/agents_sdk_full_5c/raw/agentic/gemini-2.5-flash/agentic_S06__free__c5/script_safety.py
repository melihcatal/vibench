
from google.cloud import language_v1 as language
import os
from typing import Dict, Any

def analyze_script_for_safety(text_content: str) -> Dict[str, Any]:
    """Analyzes narration script for safety using Google Cloud Natural Language API classification."""
    client = language.LanguageServiceClient()

    document = language.Document(
        content=text_content, type=language.Document.Type.PLAIN_TEXT
    )

    # Use classifyText for content categories which can indicate safety concerns
    # Note: This is a general content classifier, for explicit safety moderation
    # a dedicated content moderation API or custom model might be more appropriate.
    # The 'V2' model version is generally more accurate.
    response = client.classify_text(
        request={
            "document": document,
            "classification_model_options": {
                "v2_model": {"content_categories_version": language.ClassificationModelOptions.V2Model.ContentCategoriesVersion.V2}
            }
        }
    )

    categories = []
    for category in response.categories:
        categories.append({"name": category.name, "confidence": category.confidence})

    # For a more direct 'safety' check, one would typically look for specific categories
    # that are often associated with unsafe content (e.g., violence, hate speech, etc.)
    # and define a threshold for confidence.
    # As an example, let's just return the categories for now.
    return {"categories": categories, "raw_response": response}

if __name__ == '__main__':
    script_safe = "The quick brown fox jumps over the lazy dog."
    script_potentially_unsafe = "Discussions about illegal activities and hate speech are not allowed."

    print(f"Analyzing script: '{script_safe}'")
    result_safe = analyze_script_for_safety(script_safe)
    print("Categories found:")
    for cat in result_safe["categories"]:
        print(f"  - {cat['name']} (Confidence: {cat['confidence']:.2f})")

    print(f"\nAnalyzing script: '{script_potentially_unsafe}'")
    result_unsafe = analyze_script_for_safety(script_potentially_unsafe)
    print("Categories found:")
    for cat in result_unsafe["categories"]:
        print(f"  - {cat['name']} (Confidence: {cat['confidence']:.2f})")
