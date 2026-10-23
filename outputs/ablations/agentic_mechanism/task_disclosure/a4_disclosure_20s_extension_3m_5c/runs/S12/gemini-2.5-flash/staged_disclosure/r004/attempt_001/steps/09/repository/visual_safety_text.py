import os
import google.generativeai as genai

def check_unsafe_text(text: str):
    """
    Checks the given text for unsafe content using Google Generative AI safety settings.
    """
    try:
        # Configure the API with an API key from an environment variable
        # Replace "YOUR_API_KEY" with an actual API key or retrieve it securely.
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

        # Define safety settings
        # You can adjust these thresholds as needed for your application
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        # Initialize the Generative Model (e.g., 'gemini-pro' for text)
        model = genai.GenerativeModel('gemini-pro')

        # Generate content with safety settings applied
        response = model.generate_content(
            text,
            safety_settings=safety_settings
        )

        # Check if the response was blocked due to safety concerns
        if not response.parts:
            print(f"Text was blocked due to safety concerns: {response.prompt_feedback}")
            return True
        else:
            print("Text is safe.")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    # Example usage:
    unsafe_example = "I hate you"
    safe_example = "This is a beautiful day"

    print(f"Checking text: '{unsafe_example}'")
    is_unsafe = check_unsafe_text(unsafe_example)
    print(f"Is unsafe: {is_unsafe}\n")

    print(f"Checking text: '{safe_example}'")
    is_unsafe = check_unsafe_text(safe_example)
    print(f"Is unsafe: {is_unsafe}\n")
