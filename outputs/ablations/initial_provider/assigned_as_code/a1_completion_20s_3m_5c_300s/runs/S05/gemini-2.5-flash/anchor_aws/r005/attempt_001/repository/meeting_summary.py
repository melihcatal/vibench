import google.generativeai as genai
import os

def initialize_generative_model():
    """Initializes the Google Generative AI model client."""
    # Ensure GOOGLE_API_KEY environment variable is set
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    # Use a specific generative model for text summarization
    return genai.GenerativeModel('gemini-pro') # Provider-specific model ID

def summarize_transcript_chunk(text_chunk: str) -> str:
    """Summarizes a given chunk of meeting transcript using Google Generative AI."""
    model = initialize_generative_model()

    prompt = f"Please summarize the following meeting transcript chunk concisely:\n\n{text_chunk}\n\nSummary:"

    response = model.generate_content(prompt)
    
    # The response structure can vary, check the API documentation for specifics
    # This assumes a simple text response.
    if response.candidates and response.candidates[0].content.parts:
        return response.candidates[0].content.parts[0].text
    return "No summary generated."
