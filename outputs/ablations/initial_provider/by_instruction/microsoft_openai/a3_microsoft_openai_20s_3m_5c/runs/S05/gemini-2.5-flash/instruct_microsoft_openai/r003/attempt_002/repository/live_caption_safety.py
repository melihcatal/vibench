import os
from openai import OpenAI

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def check_safety(text: str) -> dict:
    try:
        response = openai_client.moderations.create(input=text)
        moderation_result = response.results[0]
        return {
            "flagged": moderation_result.flagged,
            "categories": moderation_result.categories.model_dump(),
            "category_scores": moderation_result.category_scores.model_dump()
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    text_to_check_safe = "This is a perfectly safe statement."
    safe_result = check_safety(text_to_check_safe)
    print(f"Safety check for \"{text_to_check_safe}\": {safe_result}")

    text_to_check_unsafe = "I want to kill myself."
    unsafe_result = check_safety(text_to_check_unsafe)
    print(f"Safety check for \"{text_to_check_unsafe}\": {unsafe_result}")
