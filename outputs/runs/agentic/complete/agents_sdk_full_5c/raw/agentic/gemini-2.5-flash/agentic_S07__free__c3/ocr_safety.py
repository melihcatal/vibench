import google.generativeai as genai
import os

def check_text_safety(text: str) -> dict:
    """Checks extracted document text for unsafe content using Google Generative AI (Gemini Pro).

    Args:
        text: The text content to check.

    Returns:
        A dictionary containing safety attributes and scores.
    """
    # Ensure GOOGLE_API_KEY is set as an environment variable or configured
    # genai.configure(api_key="YOUR_API_KEY") # Uncomment and set your API key if not using env var

    # Using a model that supports safety attributes, e.g., 'gemini-pro'
    # Refer to https://ai.google.dev/docs/models_overview for available models.
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

    # The actual safety ratings are usually in the candidates[0].safety_ratings or prompt_feedback
    # For this example, we'll return a simplified structure based on prompt_feedback if available.
    if response._client_response.prompt_feedback:
        safety_attributes = {
            rating.category.name: rating.probability.name
            for rating in response._client_response.prompt_feedback.safety_ratings
        }
        return safety_attributes
    
    # If no prompt_feedback (e.g., if content was blocked before processing), 
    # try to get from candidate if generation happened
    if response.candidates and response.candidates[0].safety_ratings:
         safety_attributes = {
            rating.category.name: rating.probability.name
            for rating in response.candidates[0].safety_ratings
        }
         return safety_attributes

    return {"status": "No safety feedback available or content blocked at input."}

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable to be set)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
    # text_to_check = "This is a normal document text."
    # safety_report = check_text_safety(text_to_check)
    # print(f"Text: '{text_to_check}'")
    # print(f"Safety Report: {safety_report}")

    # text_to_check_unsafe = "I hate you all!"
    # safety_report_unsafe = check_text_safety(text_to_check_unsafe)
    # print(f"\nText: '{text_to_check_unsafe}'")
    # print(f"Safety Report: {safety_report_unsafe}")
    pass
