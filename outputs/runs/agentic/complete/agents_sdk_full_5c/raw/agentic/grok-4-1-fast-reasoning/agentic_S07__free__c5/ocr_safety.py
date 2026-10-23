from openai import OpenAI
import os

def ocr_safety(text: str) -> bool:
    """Check extracted document text for unsafe content. Returns True if safe."""
    if not text or not text.strip():
        return True
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )
    return not response.results[0].flagged
