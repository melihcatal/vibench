import google.generativeai
import os

def check_unsafe_text(text: str) -> dict:
    """
    Checks the given text for unsafe content using Google Generative AI.

    Args:
        text: The text string to check.

    Returns:
        A dictionary containing the safety ratings from the Google Generative AI model.
    """
    # Configure Google Generative AI with API key
    # Ensure your GOOGLE_API_KEY environment variable is set
    google.generativeai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Initialize the Generative Model
    # Using a text-specific model for content safety checks
    model = google.generativeai.GenerativeModel('gemini-pro')

    response = model.generate_content(
        text,
        safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]
    )

    # The safety_ratings attribute contains the safety information
    # If the response is blocked, it will be in the prompt_feedback
    if hasattr(response, 'prompt_feedback') and response.prompt_feedback.safety_ratings:
        return {
            "is_unsafe": True,
            "safety_ratings": [
                {"category": rating.category.name, "probability": rating.probability.name}
                for rating in response.prompt_feedback.safety_ratings
            ]
        }
    elif hasattr(response, 'candidates') and response.candidates:
        # Check safety ratings of the generated content (if any was generated)
        # For simple text checks, we are more interested in prompt_feedback
        # but this is a comprehensive way to check
        all_safety_ratings = []
        for candidate in response.candidates:
            if candidate.safety_ratings:
                all_safety_ratings.extend([
                    {"category": rating.category.name, "probability": rating.probability.name}
                    for rating in candidate.safety_ratings
                ])
        return {
            "is_unsafe": bool(all_safety_ratings), # True if any safety ratings are present
            "safety_ratings": all_safety_ratings
        }
    else:
        return {"is_unsafe": False, "safety_ratings": []}

if __name__ == "__main__":
    # Example usage:
    # Set your Google API key in your environment variables before running
    # For example: export GOOGLE_API_KEY="YOUR_API_KEY"

    # Example 1: Safe text
    safe_text = "This is a beautiful image of a landscape."
    result = check_unsafe_text(safe_text)
    print(f"Safety check for '{safe_text}': {result}")

    # Example 2: Potentially unsafe text (modify to test different categories)
    # Be cautious with actual unsafe content for testing.
    # For demonstration, let's use a text that might trigger a safety flag depending on thresholds
    unsafe_text_example = "I hate this, it is really bad."
    result_unsafe = check_unsafe_text(unsafe_text_example)
    print(f"Safety check for '{unsafe_text_example}': {result_unsafe}")
