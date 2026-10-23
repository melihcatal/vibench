import os
from openai import OpenAI
from typing import List

def embed_audit_note(text: str) -> List[float]:
    """
    Embeds secret audit notes for semantic search using OpenAI Embeddings.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002" # A common embedding model from OpenAI
        )
        return response.data[0].embedding
    except Exception as e:
        raise RuntimeError(f"Error creating embedding with OpenAI: {e}")

if __name__ == '__main__':
    # This is an example of how you might use it.
    # OPENAI_API_KEY must be set as an environment variable.
    #
    # audit_note_1 = "Secret 'db_password' rotated successfully by admin@example.com on 2023-10-27."
    # audit_note_2 = "Failed attempt to access 'api_key_prod' by unauthorized IP 192.168.1.100."
    # audit_note_3 = "User 'jdoe' updated rotation policy for 'db_password' to 90 days."
    #
    # try:
    #     embedding_1 = embed_audit_note(audit_note_1)
    #     print(f"Embedding for note 1 (first 5 values): {embedding_1[:5]}...")
    #
    #     embedding_2 = embed_audit_note(audit_note_2)
    #     print(f"Embedding for note 2 (first 5 values): {embedding_2[:5]}...")
    #
    #     embedding_3 = embed_audit_note(audit_note_3)
    #     print(f"Embedding for note 3 (first 5 values): {embedding_3[:5]}...")
    #
    #     # In a real application, these embeddings would be stored in a vector database
    #     # for similarity search.
    # except RuntimeError as e:
    #     print(f"Embedding failed: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    pass
