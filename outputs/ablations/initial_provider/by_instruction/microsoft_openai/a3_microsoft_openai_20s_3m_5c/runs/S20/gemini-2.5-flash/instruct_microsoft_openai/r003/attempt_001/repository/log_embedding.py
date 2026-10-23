import os
from typing import List, Dict, Any
from observability_client import get_openai_client

def embed_log_messages(log_messages: List[str]) -> List[Dict[str, Any]]:
    """Embeds selected log messages for semantic retrieval using OpenAI Embeddings."""
    openai = get_openai_client()

    if not log_messages:
        return []

    embeddings_results = []
    for i, message in enumerate(log_messages):
        print(f"Embedding message {i+1}/{len(log_messages)}: '{message[:50]}...'")
        try:
            # OpenAI's text-embedding-ada-002 is a commonly used model for embeddings.
            response = openai.embeddings.create(
                input=message,
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding
            embeddings_results.append({
                "original_message": message,
                "embedding": embedding,
                "model": "text-embedding-ada-002"
            })
        except Exception as e:
            print(f"Error creating embedding for message '{message[:50]}...': {e}")
            embeddings_results.append({
                "original_message": message,
                "embedding": None,
                "model": "text-embedding-ada-002",
                "error": str(e)
            })
    
    print("Log message embedding completed using OpenAI Embeddings.")
    for res in embeddings_results:
        print(f"  Original: '{res['original_message'][:70]}...', Embedding size: {len(res['embedding']) if res['embedding'] else 'N/A'}")

    return embeddings_results

if __name__ == "__main__":
    # Example usage
    # Ensure OPENAI_API_KEY environment variable is set.
    os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" # Replace with your actual OpenAI API key

    if os.getenv("OPENAI_API_KEY") == "YOUR_OPENAI_API_KEY":
        print("Please set the OPENAI_API_KEY environment variable or replace the placeholder.")
    else:
        sample_log_messages = [
            "User login failed due to incorrect password.",
            "Database connection error: timeout reached.",
            "Successful user authentication.",
            "Failed login attempt from unauthorized IP address."
        ]

        embeddings = embed_log_messages(sample_log_messages)
        print("\n--- Generated Embeddings (first 5 values) ---")
        for item in embeddings:
            print(f"Original: {item['original_message'][:50]}...")
            if item['embedding']:
                print(f"Embedding (first 5): {item['embedding'][:5]}...")
            else:
                print(f"Embedding: {item.get('error', 'None')}")
            print()
