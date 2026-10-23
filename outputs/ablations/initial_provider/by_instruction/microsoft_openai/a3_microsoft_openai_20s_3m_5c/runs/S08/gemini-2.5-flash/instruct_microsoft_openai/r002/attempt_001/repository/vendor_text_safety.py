from document_client import DocumentClients
from typing import Dict, Any

def moderate_vendor_text(text_to_moderate: str) -> Dict[str, Any]:
    clients = DocumentClients()
    if not clients.openai_client:
        raise ValueError("OpenAI client not initialized.")

    if not text_to_moderate:
        return {"flagged": False, "categories": {}}

    response = clients.openai_client.moderations.create(input=text_to_moderate)
    moderation_output = response.results[0]

    return {
        "flagged": moderation_output.flagged,
        "categories": {
            category: getattr(moderation_output.categories, category)
            for category in moderation_output.categories.__dict__.keys()
            if not category.startswith('_')
        }
    }
