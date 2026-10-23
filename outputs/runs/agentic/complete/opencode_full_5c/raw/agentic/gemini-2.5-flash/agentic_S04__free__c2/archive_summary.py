import google.generativeai as genai

def summarize_transcript(transcript_text: str) -> str:
    # Ensure you have configured the Google Generative AI client with your API key
    # genai.configure(api_key="YOUR_API_KEY") 
    # For simplicity, assuming API key is configured or available via environment variables

    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for summarization
    prompt = f"Summarize the following meeting transcript:

{transcript_text}

Summary:"
    
    response = model.generate_content(prompt)
    return response.text
