from typing import Dict, Any, Optional
from document_client import get_openai_client

def moderate_vendor_notes(text: str) -> Optional[Dict[str, Any]]:
    """
    Moderates vendor notes or memo fields using Azure OpenAI's Moderation API.
    Returns the moderation API response.
    """
    client = get_openai_client()

    try:
        # OpenAI Moderation API call
        # Note: The 'moderations' object is available directly from the client for Azure OpenAI as well
        # using the correct API version and deployment configuration.
        # For simplicity, we assume a direct call if the client is configured for it.
        # If not, a specific 'moderations' client might be needed depending on SDK version and setup.
        response = client.moderations.create(input=text)
        
        # The response structure for moderations is a list of results.
        # We are interested in the first (and likely only) result for a single text input.
        if response.results:
            return response.results[0].model_dump()
        return None

    except Exception as e:
        print(f"Error moderating text: {e}")
        return None
