# vendor_text_safety.py
# Moderate vendor notes or memo fields using Perspective API (content safety)
import requests
import json
from document_models import ExpenseResponse

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

PERSPECTIVE_ENDPOINT = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def moderate_vendor_text(text: str) -> bool:
    """Return True if vendor note passes content safety checks, False otherwise.",
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
    }
    headers = {
        "Content-Type": "application/json",
        "key": PERSPECTIVE_API_KEY
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    result = response.json()
    toxicity = result['attributeScores'].get('TOXICITY', {}).get('summaryScore', {})
    score = toxicity.get('value', 0.0)
    severity = toxicity.get('summaryScore', {}).get('value', 0.0)
    # Fail if severe toxicity above threshold or toxicity above moderate threshold
    if severity > 0.9 or score > 0.7:
        return False
    return True


def moderate_expense(expense: ExpenseResponse) -> ExpenseResponse | None:
    """Moderate any free‑form notes attached to an expense.",
    # Assume free‑form notes are stored under a 'notes' key in line_items or top‑level
    notes = []
    # Pull notes from line items if present
    for item in expense.get('line_items', []):
        notes.append(item.get('description', ''))
    if 'notes' in expense:
        notes.append(expense['notes'])
    passing = all(moderate_vendor_text(note) for note in notes if note)
    return expense if passing else None
