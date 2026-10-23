import os
from openai import OpenAI

# It's recommended to use environment variables for API keys
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def moderate_claim(text_claim: str) -> dict:
    """
    Uses the OpenAI Moderation API to check if a free-text user profile claim
    violates content policies.
    
    Args:
        text_claim: The string from a user profile (e.g., bio, nickname).
        
    Returns:
        A dictionary containing the moderation result.
    """
    if not text_claim or not isinstance(text_claim, str):
        return {"flagged": False, "reason": "No text provided."}

    try:
        response = client.moderations.create(
            input=text_claim,
            # Using the latest stable moderation model
            model="text-moderation-latest" 
        )
        
        result = response.results[0]
        
        return {
            "flagged": result.flagged,
            "categories": result.categories.model_dump(),
            "category_scores": result.category_scores.model_dump(),
        }

    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return {"flagged": True, "reason": "Moderation check failed."}

if __name__ == '__main__':
    user_bio = "This is a test bio to check the moderation endpoint."
    moderation_result = moderate_claim(user_bio)
    print("Moderation result for a clean bio:", moderation_result)
    
    inappropriate_bio = "I want to buy weapons and sell drugs."
    moderation_result_flagged = moderate_claim(inappropriate_bio)
    print("Moderation result for a flagged bio:", moderation_result_flagged)
