import os
import google.generativeai as genai


def summarize_message(text: str) -> str:
    """
    Summarizes the provided text using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following text in one sentence: \n\n{text}"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return "Could not generate summary."


if __name__ == "__main__":
    sample_text = (
        "The new CRM system integration, project Titan, has been successfully deployed "
        "to the production environment ahead of schedule. All core features, including "
        "contact management, lead tracking, and sales analytics, are now live. "
        "The project team will be monitoring the system for the next 48 hours."
    )
    summary = summarize_message(sample_text)
    print(f"Original Text: {sample_text}")
    print(f"Summary: {summary}")
