import google.generativeai as genai
import os

def check_text_safety(text: str) -> bool:
    """
    Applies safety thresholds to decide whether to allow text using Google's Generative AI.
    """
    # Configure the API key. Replace with your actual API key or set as an environment variable.
    # It is recommended to use environment variables for sensitive information.
    # For example: os.environ.get("GOOGLE_API_KEY")
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY"))

    try:
        model = genai.GenerativeModel("gemini-pro") # Specify the model family

        # Define custom safety settings. These are example thresholds.
        # Adjust as needed for your application's requirements.
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_HIGH_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ]

        response = model.generate_content(
            text,
            safety_settings=safety_settings
        )

        # If the response doesn't raise an exception due to safety, it means the text is allowed.
        # You can further inspect response.prompt_feedback.safety_ratings if needed.
        if response._chunks: # Check if there is any content generated
             return True
        else:
            # If no content is generated, it implies the content was blocked.
            return False

    except Exception as e:
        # If an exception occurs, it likely means the content was blocked by safety settings
        # or there was an API error.
        print(f"Text was blocked or an error occurred: {e}")
        return False

