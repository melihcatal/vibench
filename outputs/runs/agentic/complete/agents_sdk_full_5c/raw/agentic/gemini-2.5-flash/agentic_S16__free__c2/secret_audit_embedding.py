import os
import openai
from typing import List

def embed_audit_notes(audit_notes: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using OpenAI.
    """
    # Ensure the OpenAI API key is set as an environment variable
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI()

    try:
        response = client.embeddings.create(
            input=audit_notes,
            model=model
        )
        return [data.embedding for data in response.data]
    except openai.APIAccessError as e:
        raise Exception(f"OpenAI API access error: {e}. Check your API key and permissions.")
    except openai.APIStatusError as e:
        raise Exception(f"OpenAI API status error: {e}. Status code: {e.status_code}, response: {e.response}.")
    except Exception as e:
        raise Exception(f"Failed to generate embeddings: {e}")

if __name__ == "__main__":
    # Example usage:
    # Set OPENAI_API_KEY environment variable
    # notes = [
    #     "User 'john.doe' accessed production database secret for debugging.",
    #     "Secret rotation initiated by automated system.",
    #     "Developer 'jane.smith' updated staging API key on 2023-10-26."
    # ]
    # embeddings = embed_audit_notes(notes)
    # for i, emb in enumerate(embeddings):
    #     print(f"Note {i+1} embedding (first 5 elements): {emb[:5]}...")
    #     print(f"Embedding length: {len(emb)}")
    pass
