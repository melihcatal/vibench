import google.generativeai as genai
import os

def summarize_transcription_results(transcript: str, model_name: str = "gemini-pro") -> str:
    """
    Summarizes transcription results using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel(model_name)

    prompt = f"Please summarize the following meeting transcript:

{transcript}

Summary:"

    try:
        response = model.generate_content(prompt)
        summary = response.text
        print(f"Summary generated successfully using {model_name}.")
        return summary
    except Exception as e:
        print(f"Error generating summary with Gemini API: {e}")
        return f"Error: {e}"
