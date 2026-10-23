import os
from googleapiclient import discovery
from document_models import Invoice


def vendor_text_safety(invoice: Invoice) -> dict:
    api_key = os.environ.get("GOOGLE_PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_PERSPECTIVE_API_KEY not set")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    # Assuming vendor name could be a field with user-generated content risk
    text_to_analyze = invoice.vendor_name

    analyze_request = {
        "comment": {"text": text_to_analyze},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()

        scores = {}
        for attribute, value in response["attributeScores"].items():
            scores[attribute] = value["summaryScore"]["value"]
        return scores
    except Exception as e:
        return {"error": str(e)}
