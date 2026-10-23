import requests
from document_models import ExpenseRecord

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

def moderate_vendor_notes(record: ExpenseRecord) -> ExpenseRecord:
    if not record.raw_data.get("vendor_notes"):
        return record
    notes = record.raw_data["vendor_notes"]
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        json={
            "comment": {"text": notes},
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
        },
        headers={"x-api-key": PERSPECTIVE_API_KEY}
    )
    result = response.json().get("attributeScores", {})
    toxicity = result.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    severe_toxicity = result.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    # Simple rule: if toxicity > 0.7 or severe_toxicity > 0.5, flag as unsafe
    if toxicity > 0.7 or severe_toxicity > 0.5:
        print("Vendor note flagged as unsafe (scores: toxic=%s, severe=%s)", toxicity, severe_toxicity)
        record.raw_data["vendor_notes_flagged"] = True
    return record
