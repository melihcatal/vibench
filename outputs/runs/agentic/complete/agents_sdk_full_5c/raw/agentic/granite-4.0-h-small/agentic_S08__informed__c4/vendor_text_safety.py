# [LATER-STEP] vendor_text_safety.py
from typing import Literal
import anthropic  # concrete Anthropic SDK
from document_models import InvoiceExtractionResponse

def moderate_vendor_notes(extracted: InvoiceExtractionResponse) -> Literal['safe', 'flagged']:
    """Run vendor notes through Anthropic moderation (or safety check)."
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    # Simple moderation: ask the model to flag unsafe content
    response = client.messages.create(
        model='claude-3-opus-20240229',
        max_tokens=100,
        temperature=0,
        messages=[{'role': 'user', 'content': extracted.vendor}]
    )
    # If the model output contains typical unsafe phrases, flag it
    if 'unsafe' in response.content[0].text.lower():
        return 'flagged'
    return 'safe'