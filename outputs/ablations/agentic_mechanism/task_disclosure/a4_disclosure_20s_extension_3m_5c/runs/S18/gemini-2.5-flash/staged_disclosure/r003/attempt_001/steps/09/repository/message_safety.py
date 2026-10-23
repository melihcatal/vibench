import os
import google.generativeai as genai

def check_unsafe_content(text: str) -> dict:
    """
    Checks message payload text for unsafe content using Google's Gemini API.
    """
    try:
        # Configure the API key for Google Gemini API
        # Ensure GOOGLE_API_KEY is set in your environment variables
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

        # Initialize the Generative Model
        model = genai.GenerativeModel('gemini-pro')

        # Generate content with the given text.
        # The safety settings are applied during content generation.
        response = model.generate_content(
            text,
            safety_settings={
                "HARASSMENT": "BLOCK_NONE",
                "HATE_SPEECH": "BLOCK_NONE",
                "SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "DANGEROUS_CONTENT": "BLOCK_NONE",
            },
            stream=False # Not streaming the response
        )

        # If the response was blocked due to safety concerns,
        # it will be available in prompt_feedback.
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            unsafe_categories = []
            for rating in response.prompt_feedback.safety_ratings:
                if rating.probability != 'NONE': # If probability is not NONE, it means it was evaluated
                    unsafe_categories.append({
                        "category": rating.category,
                        "probability": rating.probability
                    })
            if unsafe_categories:
                return {"unsafe_content_detected": True, "details": unsafe_categories}
        
        # If the response has candidates, it means content was generated and not blocked
        if response.candidates:
            # You can further inspect candidate.safety_ratings if you want to see
            # the safety ratings for the generated content itself, even if not blocked.
            # For this task, we are primarily interested if the *prompt* was unsafe.
            return {"unsafe_content_detected": False, "details": "No unsafe content detected in prompt."}
        
        # Fallback for unexpected scenarios
        return {"unsafe_content_detected": False, "details": "No content generated and no safety feedback."}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage:
    # Set your GOOGLE_API_KEY environment variable before running.
    # For example: export GOOGLE_API_KEY="YOUR_API_KEY"
    
    # Example 1: Safe content
    safe_text = "Hello, how are you today?"
    print(f"Checking text: '{safe_text}'")
    result = check_unsafe_content(safe_text)
    print(f"Result: {result}\n")

    # Example 2: Potentially unsafe content (replace with actual test cases as needed)
    # The actual blocking behavior depends on the model's current safety thresholds.
    unsafe_text = "I will harm you." # This is a placeholder; actual "unsafe" content needs to be chosen carefully to trigger the safety filters without violating ethical guidelines.
    print(f"Checking text: '{unsafe_text}'")
    result = check_unsafe_content(unsafe_text)
    print(f"Result: {result}\n")
