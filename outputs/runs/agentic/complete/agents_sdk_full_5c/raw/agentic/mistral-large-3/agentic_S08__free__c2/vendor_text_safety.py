from typing import Dict, Any
import requests
from document_models import InvoiceFields


def moderate_vendor_notes(invoice_data: InvoiceFields) -> Dict[str, Any]:
    """Moderate vendor notes or memo fields using Azure Content Moderator."""
    endpoint = "https://<your-azure-region>.api.cognitive.microsoft.com"
    subscription_key = "<your-subscription-key>"
    text = f"Vendor: {invoice_data.vendor}. Notes: {' '.join([item.description for item in invoice_data.line_items])}"

    response = requests.post(
        f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/Screen",
        headers={
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Content-Type": "text/plain"
        },
        data=text.encode('utf-8')
    )

    result = response.json()
    return {
        "is_flagged": result.get("Terms", []) != [],
        "flagged_terms": [term.get("Term") for term in result.get("Terms", [])]
    }