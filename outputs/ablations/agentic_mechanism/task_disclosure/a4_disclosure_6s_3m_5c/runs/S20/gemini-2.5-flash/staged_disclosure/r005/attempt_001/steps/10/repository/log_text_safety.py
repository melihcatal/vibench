import os
import google.generativeai as genai

def check_log_text_safety(log_text: str) -> dict:
    """
    Checks the given log message text for unsafe content using Google's Generative AI.

    Args:
        log_text: The log message text to check.

    Returns:
        A dictionary containing the safety analysis results.
    """
    try:
        # Configure the generative AI model with your API key
        # It is highly recommended to load the API key from environment variables
        # For example: genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        # For demonstration, we'll assume the API key is set up externally or handled by the environment.
        # Ensure your GOOGLE_API_KEY is set in your environment if running this.
        # Or, replace with your actual API key for testing (NOT RECOMMENDED FOR PRODUCTION).
        genai.configure() 

        model = genai.GenerativeModel('gemini-pro')

        # Send the text to the model for content moderation.
        # The generate_content method automatically includes safety attribute checks.
        response = model.generate_content(log_text,
                                          safety_settings=[
                                              {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                                              {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                                              {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                                              {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                                          ])

        safety_ratings = {}
        if hasattr(response, 'prompt_feedback') and hasattr(response.prompt_feedback, 'safety_ratings'):
            for rating in response.prompt_feedback.safety_ratings:
                safety_ratings[rating.category.split('_', 2)[-1]] = rating.probability.split('_', 1)[-1]
        
        is_safe = True
        if hasattr(response, 'prompt_feedback') and hasattr(response.prompt_feedback, 'block_reason'):
            is_safe = False

        return {
            "is_safe": is_safe,
            "safety_ratings": safety_ratings,
            "block_reason": response.prompt_feedback.block_reason.name if not is_safe else "N/A"
        }

    except Exception as e:
        return {"error": str(e), "is_safe": False, "safety_ratings": {}}

if __name__ == "__main__":
    # Example Usage:
    # Set your GOOGLE_API_KEY environment variable before running this example.
    # export GOOGLE_API_KEY='YOUR_API_KEY'
    
    # Example 1: Safe content
    safe_log = "User logged in successfully from IP 192.168.1.1."
    print(f"Checking safe log: '{safe_log}'")
    result_safe = check_log_text_safety(safe_log)
    print(f"Result: {result_safe}\n")

    # Example 2: Potentially unsafe content (replace with actual test case if applicable)
    # Note: Replace this with content that might trigger a safety flag for testing purposes.
    # Avoid putting genuinely harmful content here.
    unsafe_log = "This log contains some potentially harmful keywords." # Placeholder for demonstration
    print(f"Checking unsafe log: '{unsafe_log}'")
    result_unsafe = check_log_text_safety(unsafe_log)
    print(f"Result: {result_unsafe}\n")
