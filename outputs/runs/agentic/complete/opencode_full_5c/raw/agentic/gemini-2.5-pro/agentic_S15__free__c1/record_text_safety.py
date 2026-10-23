import os
from googleapiclient import discovery
from database_models import Document


def record_text_safety(document: Document) -> dict:
    """
    Checks the document content for unsafe content using Google's Perspective API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": document.content},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    return {"toxicity_score": toxicity_score}
