import os
from openai import OpenAI

def platform_output_safety(text: str) -> dict:
    """
    Checks platform model output for unsafe content using OpenAI's Moderation API.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
    )
    
    response = client.moderations.create(input=text)
    moderation_result = response.results[0]
    
    return moderation_result.model_dump()
