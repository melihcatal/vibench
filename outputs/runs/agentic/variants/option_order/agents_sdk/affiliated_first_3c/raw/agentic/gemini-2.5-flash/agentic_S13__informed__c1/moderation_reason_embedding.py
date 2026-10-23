import os
import google.generativeai as genai

def moderation_reason_embedding(rationale_text: str):
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('embedding-001')

    response = model.embed_content(model_name="models/embedding-001", content=rationale_text)
    return response['embedding']
