import os
from googleapiclient import discovery
from database_models import Document


def check_document_safety(document: Document) -> dict:
    """
    Checks user-generated document fields for unsafe content using Google's Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": document.get("content", "")},
        "requestedAttributes": {"TOXICITY": {}},
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"][
            "value"
        ]
        return {
            "document_id": document.get("document_id"),
            "toxicity_score": toxicity_score,
            "is_safe": toxicity_score < 0.7,
        }
    except Exception as e:
        return {"error": f"Perspective API request failed: {e}"}
