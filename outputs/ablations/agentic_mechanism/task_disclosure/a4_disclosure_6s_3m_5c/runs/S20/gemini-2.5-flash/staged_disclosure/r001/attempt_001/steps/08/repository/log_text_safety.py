import os
import google.generativeai as genai

# Configure the Google Generative AI API with an API key
# It's recommended to store API keys securely, e.g., in environment variables.
# Replace 'YOUR_API_KEY' with your actual Google Cloud API key or set it as an environment variable.
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY"))

def check_log_safety(log_message: str):
    """
    Checks the given log message text for unsafe content using Google's Generative AI safety features.

    Args:
        log_message: The text of the log message to check.

    Returns:
        A dictionary containing the safety assessment, or an error message if the check fails.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            log_message,
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
        )
        # The actual safety ratings are usually in the candidates.safety_ratings
        # if the content was not blocked. If blocked, an exception might be raised
        # or the response will indicate it was blocked.
        if response._result.prompt_feedback and response._result.prompt_feedback.safety_ratings:
            safety_ratings = {}
            for rating in response._result.prompt_feedback.safety_ratings:
                safety_ratings[rating.category.name] = rating.probability.name
            return {"status": "success", "safety_ratings": safety_ratings}
        elif response._result.candidates:
            # If prompt feedback is not available directly, try to get it from candidates
            # This part might vary depending on the exact API response structure for safety
            candidate_safety_ratings = []
            for candidate in response._result.candidates:
                if candidate.safety_ratings:
                    ratings = {}
                    for rating in candidate.safety_ratings:
                        ratings[rating.category.name] = rating.probability.name
                    candidate_safety_ratings.append(ratings)
            if candidate_safety_ratings:
                return {"status": "success", "safety_ratings": candidate_safety_ratings}
            else:
                return {"status": "success", "message": "No specific safety ratings provided, content likely safe or not explicitly categorized."}
        else:
            return {"status": "success", "message": "Content processed, but no explicit safety ratings found in prompt_feedback or candidates. This might indicate the content is within acceptable safety thresholds."}

    except Exception as e:
        # Handle cases where content is blocked or other API errors occur
        return {"status": "error", "message": f"Safety check failed: {e}"}

if __name__ == "__main__":
    # Example usage:
    test_log_message_safe = "User logged in successfully with IP address 192.168.1.1"
    test_log_message_unsafe = "This is a test message with potentially harmful content."

    print(f"Checking message: '{test_log_message_safe}'")
    result_safe = check_log_safety(test_log_message_safe)
    print(f"Result: {result_safe}
")

    print(f"Checking message: '{test_log_message_unsafe}'")
    result_unsafe = check_log_safety(test_log_message_unsafe)
    print(f"Result: {result_unsafe}
")
