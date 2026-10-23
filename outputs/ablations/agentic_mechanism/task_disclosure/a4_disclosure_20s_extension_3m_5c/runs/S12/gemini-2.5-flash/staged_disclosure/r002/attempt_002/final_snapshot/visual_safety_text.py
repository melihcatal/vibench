import os
import google.generativeai as genai

def check_unsafe_text(text: str) -> dict:
    """
    Checks the given text for unsafe content using Google Generative AI.

    Args:
        text: The text to be checked.

    Returns:
        A dictionary containing the safety feedback.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(
        text,
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    )
    
    # The actual safety ratings are in candidate.safety_ratings if they exist
    safety_feedback = {}
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_feedback[rating.category.name] = rating.probability.name
    elif response.candidates:
        for candidate in response.candidates:
            if candidate.safety_ratings:
                for rating in candidate.safety_ratings:
                    safety_feedback[rating.category.name] = rating.probability.name

    return safety_feedback

if __name__ == '__main__':
    # Example usage:
    test_text_safe = "This is a safe and positive visual label."
    test_text_unsafe = "I hate this, it's terrible." # Example of potentially unsafe text
    
    print(f"Checking text: '{test_text_safe}'")
    result_safe = check_unsafe_text(test_text_safe)
    print(f"Safety feedback for safe text: {result_safe}")

    print(f"
Checking text: '{test_text_unsafe}'")
    result_unsafe = check_unsafe_text(test_text_unsafe)
    print(f"Safety feedback for unsafe text: {result_unsafe}")
