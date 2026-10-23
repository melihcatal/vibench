import os
from openai import OpenAI

def check_platform_output_safety(text: str):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    response = client.moderations.create(input=text)
    # The moderation API returns a list of results, typically one per input string
    # For a single string input, we check the first result
    moderation_result = response.results[0]
    
    # If flagged is true, it means the content violates OpenAI's usage policies.
    # You can also inspect individual category scores if needed.
    return {
        "flagged": moderation_result.flagged,
        "categories": moderation_result.categories.model_dump(),
        "category_scores": moderation_result.category_scores.model_dump()
    }
