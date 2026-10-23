import os
import google.generativeai as genai

# Google Gemini API provider-identifying signal: google.generativeai


def summarize_message(text: str) -> str:
    """Summarizes message content using the Google Gemini API."""
    # Ensure the GOOGLE_API_KEY environment variable is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Use a specific model that supports text generation. `gemini-pro` is a good general-purpose choice.
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        f"Please provide a concise summary of the following text:\n\n{text}\n\nSummary:"
    )

    response = model.generate_content(prompt)

    if response.candidates:
        # Access the text from the first part of the first candidate
        summary = response.candidates[0].content.parts[0].text
        return summary
    else:
        return "Failed to generate summary."
