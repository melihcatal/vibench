import google.generativeai as genai
import os

def summarize_transcript_chunk(transcript_chunk: str) -> str:
    """
    Summarizes a live meeting transcript chunk using the Google Gemini API.
    Service: Google Gemini API
    SDK: google-genai
    Auth: GOOGLE_API_KEY (from environment variable)
    Model: gemini-pro (concrete model identifier)
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro') # Concrete model identifier

    prompt = f"Summarize the following meeting transcript chunk:

{transcript_chunk}"
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY environment variable is set.
    # The SDK is google-genai
    # The model is identified by 'gemini-pro'
    
    chunk1 = "The first quarter results were discussed. Sales are up by 15% and profits increased by 10%. We need to focus on marketing for the next quarter. John suggested a new social media campaign. Sarah agreed and will draft a proposal."
    summary1 = summarize_transcript_chunk(chunk1)
    print(f"Chunk 1: {chunk1}")
    print(f"Summary 1: {summary1}\n")

    chunk2 = "Technical discussion about the new microservice architecture. Decided to use Kubernetes for deployment. Database migration will be handled by the backend team. Frontend team needs to integrate with the new API endpoints by next month."
    summary2 = summarize_transcript_chunk(chunk2)
    print(f"Chunk 2: {chunk2}")
    print(f"Summary 2: {summary2}")
