import os
import google.generativeai as genai

def embed_script(text: str) -> dict:
    # Ensure the Google API key is set as an environment variable or passed securely
    # For this example, we assume `GOOGLE_API_KEY` is set in the environment.
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    # Use a pre-configured model for embeddings
    # For example, using a text-embedding-004 model
    # Model identifiers are provider-specific.
    try:
        response = genai.embed_content(model="models/embedding-001", content=text)
        return {"embedding": response['embedding']}
    except Exception as e:
        raise RuntimeError(f"Google Generative AI embedding failed: {e}")
