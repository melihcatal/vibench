import os
import google.generativeai as genai

def summarize_text(text: str, model_name: str = 'gemini-pro') -> str:
    # Configure the Gemini API client
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    if not genai.get_default_model():
        print("Google API Key not configured or model not set.")
        return ""

    model = genai.GenerativeModel(model_name)

    try:
        prompt = f"Summarize the following text:

{text}

Summary:"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing text with Gemini API: {e}")
        return ""

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    long_transcript = (
        "The meeting started at 10 AM. John presented the Q3 sales figures, which showed a 15% increase "
        "over Q2. Sarah then discussed the marketing strategy for the upcoming product launch, focusing "
        "on social media campaigns and influencer partnerships. David raised concerns about the budget "
        "for the marketing initiatives, suggesting a review of the proposed ad spend. Emily proposed "
        "a follow-up meeting to finalize the budget and allocate resources. The meeting concluded at "
        "11 AM with an agreement to reconvene next Tuesday."
    )

    summary = summarize_text(long_transcript)
    print(f"Original Transcript:\n{long_transcript}\n")
    print(f"Summary:\n{summary}")
