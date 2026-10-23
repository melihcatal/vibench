import os
from langchain_openai import OpenAIEmbeddings

def embed_audit_notes(notes: list[str]) -> list[list[float]]:
    """
    Embeds a list of secret audit notes using OpenAI embeddings for semantic search.

    Args:
        notes: A list of strings, where each string is an audit note.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    # Initialize OpenAIEmbeddings. Ensure OPENAI_API_KEY is set in your environment variables.
    # The concrete external provider is OpenAI.
    embeddings_model = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

    # Generate embeddings for the notes
    embeddings = embeddings_model.embed_documents(notes)

    return embeddings

if __name__ == "__main__":
    # Example usage
    audit_notes = [
        "Audit revealed an unencrypted S3 bucket storing sensitive data.",
        "Detected a hardcoded API key in the authentication module.",
        "Review of access logs showed unusual activity from an external IP.",
        "Implemented multi-factor authentication for all administrative accounts.",
        "Patched critical vulnerability in the web application firewall."
    ]

    # To run this example, you need to set your OPENAI_API_KEY environment variable:
    # export OPENAI_API_KEY="your_openai_api_key_here"
    # or
    # os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"

    # For demonstration purposes, if the API key is not set, we'll print a message.
    if os.environ.get("OPENAI_API_KEY"):
        note_embeddings = embed_audit_notes(audit_notes)
        print(f"Generated {len(note_embeddings)} embeddings.")
        for i, embedding in enumerate(note_embeddings):
            print(f"Note {i+1} embedding (first 5 elements): {embedding[:5]}...")
    else:
        print("OPENAI_API_KEY environment variable not set. Please set it to run the example.")
