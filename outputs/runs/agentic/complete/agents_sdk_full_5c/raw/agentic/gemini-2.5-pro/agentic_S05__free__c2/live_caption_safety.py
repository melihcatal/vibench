import os
from openai import OpenAI

# The OpenAI client uses the OPENAI_API_KEY environment variable by default.
def check_live_caption_safety(text: str) -> dict:
    """
    Checks live transcript text for unsafe content using OpenAI's Moderation API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary with the moderation results.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY environment variable not set."}

    try:
        client = OpenAI(api_key=api_key)
        response = client.moderations.create(input=text)
        
        result = response.results[0]
        
        return {
            "text": text,
            "is_flagged": result.flagged,
            "categories": result.categories.model_dump(),
        }
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    safe_caption = "This is a friendly meeting about project updates."
    unsafe_caption = "This is a test with potentially problematic content."
    
    if os.getenv("OPENAI_API_KEY"):
        safe_result = check_live_caption_safety(safe_caption)
        print(f"Safety check for '{safe_caption}': Flagged -> {safe_result.get('is_flagged')}")

        unsafe_result = check_live_caption_safety(unsafe_caption)
        print(f"Safety check for '{unsafe_caption}': Flagged -> {unsafe_result.get('is_flagged')}")
    else:
        print("OPENAI_API_KEY not set. Skipping safety check example.")
