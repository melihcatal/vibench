import os
from openai import OpenAI

def vendor_text_safety(text: str) -> bool:
    """
    Moderate vendor notes/memo fields using OpenAI Moderation API.
    Returns True if the content is safe, False otherwise.
    """
    if not text:
        return True  # empty is safe
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=text, model="moderation-latest")
    flagged = any(item["flagged"] for item in response["results"])
    return not flagged
