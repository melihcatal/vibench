from google.cloud import generative_ai
import os

def summarize_moderation_decisions(decisions: list[str]) -> str:
    """
    Summarizes a list of moderation decisions using a Google Cloud Generative AI model.

    Args:
        decisions: A list of strings, where each string represents a moderation decision.

    Returns:
        A string containing the summary of the moderation decisions.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    # For local development, you might set it directly or load from a .env file.
    # In a production environment, consider using Google Cloud authentication mechanisms.
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")

    prompt = "Summarize the following moderation decisions:
"
    for i, decision in enumerate(decisions):
        prompt += f"{i+1}. {decision}
"
    prompt += "\nProvide a concise summary highlighting the key themes and outcomes."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing decisions: {e}"

