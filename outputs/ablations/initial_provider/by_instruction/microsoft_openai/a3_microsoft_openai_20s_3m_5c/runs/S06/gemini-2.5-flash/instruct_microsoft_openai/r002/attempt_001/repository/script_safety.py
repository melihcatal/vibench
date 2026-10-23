from openai import OpenAI
import os

def check_script_safety(text: str) -> dict:
    """
    Checks narration scripts for unsafe content using OpenAI Moderation API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(input=text)
    
    # The moderation API may return multiple results if the input is an array of strings.
    # For a single string input, it typically returns one result.
    moderation_result = response.results[0]
    
    return {
        "flagged": moderation_result.flagged,
        "categories": {category.category: category.score for category in moderation_result.categories if category.triggered}
    }
