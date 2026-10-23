import google.generativeai as genai
import os
from observability_models import SafetyCheckRequest, SafetyCheckResponse

def check_log_text_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """
    Checks selected log message text for unsafe content using Google Gemini Pro's safety settings.

    Args:
        request: A SafetyCheckRequest object containing the text to be checked.

    Returns:
        A SafetyCheckResponse object indicating if the content is safe and providing safety ratings.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    # The generative model inherently applies safety filters. We can query the safety ratings.
    try:
        response = model.generate_content(request.text, 
                                          safety_settings={
                                              'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                                              'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                                              'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                                              'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
                                          })
        
        # If the content was blocked, response.text might be empty or raise an exception on access
        # We explicitly check for prompt_feedback which indicates if any safety attribute was blocked
        is_safe = True
        safety_ratings = {}

        if response._chunks and response._chunks[0].safety_ratings:
            for rating in response._chunks[0].safety_ratings:
                safety_ratings[rating.category.name] = rating.probability.name
                if rating.probability > genai.types.HarmProbability.NEGLIGIBLE:
                    is_safe = False

        # If the generation was blocked entirely due to safety, response.text will not exist
        # and response.prompt_feedback will contain the reason.
        if not response._chunks or response.prompt_feedback.block_reason:
             is_safe = False
             if response.prompt_feedback.safety_ratings:
                 for rating in response.prompt_feedback.safety_ratings:
                     safety_ratings[rating.category.name] = rating.probability.name

        return SafetyCheckResponse(is_safe=is_safe, safety_ratings=safety_ratings)

    except Exception as e:
        # This can happen if the input itself triggers a block before generation starts
        safety_ratings_from_exception = {}
        if hasattr(e, 'response') and hasattr(e.response, 'prompt_feedback') and hasattr(e.response.prompt_feedback, 'safety_ratings'):
            for rating in e.response.prompt_feedback.safety_ratings:
                safety_ratings_from_exception[rating.category.name] = rating.probability.name
        return SafetyCheckResponse(is_safe=False, safety_ratings=safety_ratings_from_exception)

if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY environment variable is set for this example to run
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    print("\n--- Safety Check 1 (Safe Content) ---")
    safe_text_request = SafetyCheckRequest(text="User logged in successfully from IP 192.168.1.10.")
    try:
        safe_response = check_log_text_safety(safe_text_request)
        print(f"Text: \"{safe_text_request.text}\"")
        print(f"Is Safe: {safe_response.is_safe}")
        print(f"Safety Ratings: {safe_response.safety_ratings}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Safety Check 2 (Potentially Unsafe Content - example) ---")
    # Note: The actual classification depends on the model's internal logic.
    # This is an illustrative example.
    unsafe_text_request = SafetyCheckRequest(text="Bad user trying to inject malicious SQL query: 'DROP TABLE users;'")
    try:
        unsafe_response = check_log_text_safety(unsafe_text_request)
        print(f"Text: \"{unsafe_text_request.text}\"")
        print(f"Is Safe: {unsafe_response.is_safe}")
        print(f"Safety Ratings: {unsafe_response.safety_ratings}")
    except Exception as e:
        print(f"Error: {e}")
