from google.cloud import generative_ai as genai
import os

def summarize_record(document_content, config=None):
    config = config or {}
    
    # Use environment variable for API key or provide in config
    genai.configure(api_key=config.get('google_api_key', os.environ.get('GOOGLE_API_KEY')))

    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro as a concrete model identifier
    
    prompt = f"Please summarize the following document content:\n\n{document_content}"
    response = model.generate_content(prompt)
    
    return {"summary": response.text}
