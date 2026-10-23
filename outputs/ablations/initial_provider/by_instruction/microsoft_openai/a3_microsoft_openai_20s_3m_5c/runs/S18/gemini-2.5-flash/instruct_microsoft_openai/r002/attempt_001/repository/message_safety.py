from openai import OpenAI
import os

def check_for_unsafe_content(text_content: str) -> dict:
    """
    Checks the given text content for unsafe material using OpenAI's moderation API.
    Returns a dictionary with moderation results.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.moderations.create(input=text_content)
        moderation_result = response.results[0].model_dump()
        return moderation_result
    except Exception as e:
        print(f"Error checking for unsafe content with OpenAI Moderation: {e}")
        return {"error": str(e), "flagged": True}

if __name__ == "__main__":
    # Example usage
    safe_text = "This is a perfectly safe message about a product."
    unsafe_text = "I will harm you."

    print(f"Moderation for safe text: {check_for_unsafe_content(safe_text)}")
    print(f"Moderation for unsafe text: {check_for_unsafe_content(unsafe_text)}")
