import json
from pathlib import Path
from google.genai import ServiceContext, SecretAgent


def embed_secret_audit(note: str, model_id: str = "gemini-flash") -> str:
    """Embed secret audit notes using Google Gemini to enable semantic search."""
    service_context = ServiceContext.from_defaults(model=model_id)
    agent = SecretAgent(service_context=service_context)
    # Store the note as an embedding (placeholder implementation)
    response = agent.embed_message(note)
    # Return a JSON blob for downstream indexing
    return json.dumps({"embedding": response.embedding, "note": note})


if __name__ == "__main__":
    note = Path("audit_note.txt").read_text()
    print(embed_secret_audit(note))
