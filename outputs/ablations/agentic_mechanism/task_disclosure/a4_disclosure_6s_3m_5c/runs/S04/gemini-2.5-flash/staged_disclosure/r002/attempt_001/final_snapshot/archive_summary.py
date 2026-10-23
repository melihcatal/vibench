import google.generativeai
import os

def summarize_transcription(transcription_text: str) -> str:
    """Summarizes transcription results using Google's Generative AI."""
    try:
        google.generativeai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "GOOGLE_API_KEY environment variable not set. Please set it to use this function."

    model = google.generativeai.GenerativeModel('gemini-pro')
    prompt = f"Please summarize the following transcription:

{transcription_text}"
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (replace with actual transcription data)
    sample_transcription = """
    This is a sample transcription of a meeting. The main points discussed were the new project launch,
    which is scheduled for next quarter, and the budget allocation for marketing. Sarah mentioned
    that the team needs to finalize the design mockups by Friday. John brought up concerns about
    resource availability, and it was decided that a follow-up meeting would be held to address this.
    The overall sentiment was positive, despite the challenges.
    """
    summary = summarize_transcription(sample_transcription)
    print("Summary:")
    print(summary)
