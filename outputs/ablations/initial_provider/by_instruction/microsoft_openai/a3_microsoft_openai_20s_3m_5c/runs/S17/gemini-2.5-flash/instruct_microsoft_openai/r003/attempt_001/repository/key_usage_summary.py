from security_client import SecurityClient
from security_models import AuditNote
from typing import List
import json

def summarize_key_usage(audit_notes: List[AuditNote]) -> str:
    """Summarizes key usage and crypto events using Azure OpenAI for analysis."""
    security_client = SecurityClient("https://unused.vault.azure.net") # Placeholder URL, not used for OpenAI
    openai_client = security_client.get_openai_client()

    # Prepare the audit notes for the LLM
    notes_str = "\n".join([f"Event Type: {note.event_type}, Details: {note.details}, Key ID: {note.key_id}, Timestamp: {note.timestamp}" for note in audit_notes])

    prompt = f"""Analyze the following cryptographic audit notes and provide a concise summary of key usage patterns, potential anomalies, and overall security posture. Focus on the types of operations, which keys are being used, and any notable events.

Audit Notes:
{notes_str}

Summary:"""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-35-turbo",  # Specify a concrete model ID for Azure OpenAI
            messages=[
                {"role": "system", "content": "You are a security analyst summarizing cryptographic audit logs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing key usage: {str(e)}"

