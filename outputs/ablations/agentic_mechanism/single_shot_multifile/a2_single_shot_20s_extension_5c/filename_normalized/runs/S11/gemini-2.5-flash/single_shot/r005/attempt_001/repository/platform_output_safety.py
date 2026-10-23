import os
from google.cloud import language_v1
from typing import Dict, Any

def check_platform_output_safety(text_content: str) -> Dict[str, Any]:
    """Check platform model output for unsafe content using Google Cloud Natural Language API."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise for Google Cloud.
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # The classify_text method can give a high-level categorization,
    # which can be indicative of certain types of content (e.g., adult, violence).
    # For more granular safety checks, Google Cloud's Perspective API is often used,
    # but for a general safety check, Natural Language API's classification is a viable option.
    try:
        response = client.classify_text(request={'document': document})
        
        safety_analysis = {"categories": []}
        for category in response.categories:
            safety_analysis["categories"].append({
                "name": category.name,
                "confidence": category.confidence
            })
        return safety_analysis
    except Exception as e:
        raise RuntimeError(f"Google Cloud Natural Language API content classification failed: {e}")
