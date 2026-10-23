import os
import google.generativeai as genai

def embed_text(text: str) -> list[float]:
    # Make sure to configure your API key for Google Generative AI
    # genai.configure(api_key="YOUR_API_KEY")
    try:
        model = genai.GenerativeModel('models/embedding-001')
        result = model.embed_content(text, task_type="RETRIEVAL_DOCUMENT")
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        print("Please ensure the Google Generative AI API key is configured and accessible.")
        return []

def secret_audit_embedding(audit_note: str) -> list[float]:
    return embed_text(audit_note)

if __name__ == '__main__':
    sample_audit_note = "API key rotation initiated by user_X due to compromise alert."
    # embedding = secret_audit_embedding(sample_audit_note)
    # print(f"Embedding for audit note: {embedding[:5]}...") # Print first 5 elements
