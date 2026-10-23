import google.generativeai as genai
from security_models import AuditNote
from typing import List, Dict, Any
import os

def embed_audit_notes(audit_notes: List[AuditNote]) -> List[Dict[str, Any]]:
    # Ensure the Google API key is set as an environment variable or configured
    # For this example, we assume GOOGLE_API_KEY is set.
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    embedded_notes = []
    for note in audit_notes:
        # The embedding model is typically specified here.
        # Using a common embedding model like 'models/embedding-001'
        response = genai.embed_content(
            model="models/embedding-001",
            content=note.content,
            task_type="RETRIEVAL_DOCUMENT"
        )
        embedded_notes.append({
            "note_id": note.note_id,
            "secret_id": note.secret_id,
            "embedding": response['embedding']
        })
    return embedded_notes
