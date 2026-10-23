import google.generativeai as genai
import os
from typing import List, Dict, Any

# Assuming observability_client and observability_models exist and are in the same directory or importable path
from observability_client import get_project_id, get_logging_v2_client
from observability_models import LogQueryParameters

def embed_log_messages(
    project_id: str,
    log_name: str,
    time_range_minutes: int = 60,
    model_name: str = "models/embedding-001", # Concrete embedding model identifier for Gemini
) -> List[Dict[str, Any]]:
    """Embeds selected log messages for semantic retrieval using the Google Gemini Embeddings API.
    Fetches recent logs from a specified log_name and generates embeddings for their messages.
    """
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return [{"error": "GOOGLE_API_KEY environment variable not set. Cannot access Gemini API."}]
    
    logging_client = get_logging_v2_client(project_id)

    # Fetch recent logs from the specified log_name
    query_params = LogQueryParameters(
        project_id=project_id,
        time_range_minutes=time_range_minutes,
        log_name=log_name
    )
    filter_str = query_params.to_gcp_filter_string()

    logs_to_embed = []
    for entry in logging_client.list_entries(order_by=logging_v2.LogEntryOrder.NEWEST, filter_=filter_str, page_size=50): # Limit logs to process
        message = entry.text_payload if entry.text_payload else (entry.json_payload.get("message") if entry.json_payload else None)
        if message:
            logs_to_embed.append({
                "log_id": entry.insert_id,
                "timestamp": str(entry.timestamp),
                "message": message,
            })

    if not logs_to_embed:
        print(f"No recent logs found in '{log_name}' for embedding.")
        return []

    embedded_logs = []
    # The Gemini API embedding model can take a list of texts (up to a certain limit)
    # It's more efficient to batch these requests.
    messages_to_embed = [log["message"] for log in logs_to_embed]

    if not messages_to_embed:
        return []
    
    try:
        # Call the embedding model
        # The generate_embeddings method expects a list of content parts
        # For simple text, it's typically just {'parts': [{'text': 'your text here'}]}]
        
        # Process in chunks to avoid hitting API limits for large number of texts
        chunk_size = 50 # Adjust based on API limits and performance needs
        for i in range(0, len(messages_to_embed), chunk_size):
            chunk_messages = messages_to_embed[i:i + chunk_size]
            
            # The SDK handles the structure for `embed_content` or `generate_embeddings`
            # For `embed_content` which is the typical method for text, it expects `model` and `content`.
            # `content` can be a string, a list of strings, or a `Part` or a list of `Part`s.
            # When `content` is a list of strings, it will treat each string as a separate item to embed.
            
            batch_response = genai.embed_content(
                model=model_name,
                content=chunk_messages,
                task_type="RETRIEVAL_DOCUMENT" # Specify task type for better embeddings
            )

            for j, embedding_data in enumerate(batch_response['embeddings']):
                original_log_index = i + j
                embedded_logs.append({
                    "log_id": logs_to_embed[original_log_index]["log_id"],
                    "timestamp": logs_to_embed[original_log_index]["timestamp"],
                    "message": logs_to_embed[original_log_index]["message"],
                    "embedding": embedding_data['values'], # The actual list of floats
                })

    except Exception as e:
        print(f"Error calling Gemini Embeddings API: {e}")
        return [{"error": f"Error generating embeddings: {e}"}]

    return embedded_logs

if __name__ == "__main__":
    project_id = get_project_id()
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
        exit(1)

    log_name_to_embed = "my-app-logs" # Replace with a log name containing messages to embed
    # Ensure GOOGLE_API_KEY is set in your environment variables.

    print(f"Generating embeddings for log messages from '{log_name_to_embed}'...")
    embeddings_results = embed_log_messages(project_id=project_id, log_name=log_name_to_embed, time_range_minutes=60)

    if embeddings_results:
        print("\n--- Log Message Embeddings ---")
        for result in embeddings_results:
            print(f"Log ID: {result['log_id']}")
            print(f"Message: {result['message']}")
            print(f"Embedding (first 5 values): {result['embedding'][:5]}...")
            print(f"Embedding dimension: {len(result['embedding'])}")
            print("---")
    else:
        print("No logs were embedded or found.")
