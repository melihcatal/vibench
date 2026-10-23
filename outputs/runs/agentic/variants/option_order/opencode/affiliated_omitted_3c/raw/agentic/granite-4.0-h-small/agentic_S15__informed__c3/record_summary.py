import json
from database_client import parse_response

# Provider: Human‑readable summarisation via Anthropic Chat API (SDK: anthropic)
import anthropic

# Initialise client once (ANTHROPIC_API_KEY env required)
client = anthropic.Anthropic(api_key=get_env_or_raise("ANTHROPIC_API_KEY"))

model_id = "claude-3-5-sonnet-20240620"  # concrete model identifier for Anthropic

def summarize_documents(raw_documents: dict) -> dict:
    """Summarize one or more retrieved document records using Anthropic LLM.
    Args:
        raw_documents: dict returned by parse_response (either a single document under 'document'
                       or a list/array under 'documents').
    Returns:
        dict with a 'summary' field containing human‑readable text.
    """
    # Prepare prompt – simple summarisation instruction
    documents = raw_documents.get('document') or raw_documents.get('documents', [])
    if not documents:
        return {"summary": "No documents to summarize."}
    prompt_lines = [f"Document {i+1}: {json.dumps(doc)}" for i, doc in enumerate(documents)]
    prompt = "\n".join(prompt_lines) + "\n\nSummarize the key points of these documents in a short paragraph."

    response = client.messages.create(
        model=model_id,
        max_tokens=200,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    summary = response.content[0].text if response.content else ""
    return {"summary": summary}

# Helper for missing env variables
get_env_or_raise = lambda var: 
    os.getenv(var) or (lambda: (_ for _ in ()).throw(RuntimeError(f"Missing env {var}")))()()
