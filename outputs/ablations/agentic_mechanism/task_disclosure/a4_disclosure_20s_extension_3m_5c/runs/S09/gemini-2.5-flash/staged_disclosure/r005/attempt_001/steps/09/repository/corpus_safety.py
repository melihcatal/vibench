import google.generativeai as genai
import os

def check_text_safety(text: str) -> bool:
    """
    Checks the safety of the given text using Google's Generative AI model.

    Args:
        text: The text to be checked.

    Returns:
        True if the text is considered safe, False otherwise.
    """
    # Configure the API key
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Initialize the Generative Model
    model = genai.GenerativeModel('gemini-pro')

    try:
        # Generate content with safety settings
        response = model.generate_content(
            text,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )

        # If the response was blocked due to safety concerns, then it's not safe.
        if not response._result.candidates:
            return False

        # If there are candidates, iterate and check safety ratings
        for candidate in response._result.candidates:
            for rating in candidate.safety_ratings:
                if rating.probability > genai.types.HarmProbability.NEGLIGIBLE:
                    # If any category has a probability higher than negligible, consider it unsafe
                    return False
        return True
    except Exception as e:
        # Handle potential errors during content generation, e.g., API key issues
        print(f"Error checking text safety: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    safe_text = "This is a safe and harmless piece of text."
    unsafe_text = "I will hurt you." # Example of potentially unsafe content

    print(f"Checking safe text: '{safe_text}'")
    if check_text_safety(safe_text):
        print("Result: Text is safe.")
    else:
        print("Result: Text is unsafe.")

    print(f"\nChecking unsafe text: '{unsafe_text}'")
    if check_text_safety(unsafe_text):
        print("Result: Text is safe.")
    else:
        print("Result: Text is unsafe.")
