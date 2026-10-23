import google.generativeai as genai

def secret_audit_embedding(audit_notes: str, config: dict) -> dict:
    genai.configure(api_key=config.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') # Using a generative model, but for embeddings we use specific embedding models
    
    # For embeddings, we typically use the 'embedding-001' model.
    # The genai.embed_content function is the correct way to get embeddings.
    response = genai.embed_content(
        model="models/embedding-001",
        content=audit_notes,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return {"embedding": response['embedding']}
