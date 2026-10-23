import google.generativeai as genai
import os

def check_for_unsafe_text(labels: dict, notes: str) -> bool:
    """
    Checks secret labels and notes for unsafe text using Google Cloud Generative AI.

    Args:
        labels: A dictionary of secret labels.
        notes: A string containing secret notes.

    Returns:
        True if unsafe text is detected, False otherwise.
    """
    # Configure the Generative AI client
    # It's assumed that GOOGLE_API_KEY is set in the environment variables
    # For production, consider more secure ways to handle API keys.
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        print("GOOGLE_API_KEY environment variable not set. Please set it to use the Generative AI API.")
        return False

    model = genai.GenerativeModel('gemini-pro')

    combined_text = f"Labels: {labels}\nNotes: {notes}"

    try:
        response = model.generate_content(
            combined_text,
            safety_settings={
                'HARASSMENT': 'BLOCK_LOW_AND_ABOVE',
                'HATE_SPEECH': 'BLOCK_LOW_AND_ABOVE',
                'SEXUALLY_EXPLICIT': 'BLOCK_LOW_AND_ABOVE',
                'DANGEROUS_CONTENT': 'BLOCK_LOW_AND_ABOVE',
            }
        )

        # If the response contains a prompt_feedback attribute and it has a BlockReason,
        # it indicates that the content was blocked due to safety concerns.
        if response.prompt_feedback and response.prompt_feedback.block_reason:
            return True
        return False

    except Exception as e:
        print(f"An error occurred while checking for unsafe text: {e}")
        return False
