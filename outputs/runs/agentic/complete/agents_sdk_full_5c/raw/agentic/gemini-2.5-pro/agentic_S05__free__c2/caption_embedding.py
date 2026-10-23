import os
import requests

# Using a specific sentence-transformer model from the Hugging Face Hub
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def get_caption_embedding(text: str) -> dict:
    """
    Embeds a caption chunk using a Hugging Face Inference API model.

    Args:
        text: The caption text to embed.

    Returns:
        A dictionary containing the embedding vector or an error.
    """
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        return {"error": "HF_TOKEN environment variable not set."}

    headers = {"Authorization": f"Bearer {hf_token}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={
            "inputs": [text],
            "options": {"wait_for_model": True}
        })
        response.raise_for_status()
        
        json_response = response.json()
        
        # The API returns a list of embeddings, one for each input string.
        # Since we send one string, we take the first element.
        if isinstance(json_response, list) and len(json_response) > 0:
             return {
                "text": text,
                "embedding": json_response[0]
            }
        else:
            return {"error": "Unexpected response format from Hugging Face API.", "details": json_response}

    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Hugging Face API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    caption = "The new feature will be deployed next Tuesday."
    
    if os.getenv("HF_TOKEN"):
        embedding_result = get_caption_embedding(caption)
        if "embedding" in embedding_result:
            embedding_vector = embedding_result["embedding"]
            print(f"Text: '{embedding_result['text']}'")
            print(f"Embedding vector dimension: {len(embedding_vector)}")
            print(f"Embedding vector (first 5 values): {embedding_vector[:5]}")
        else:
            print(f"Failed to get embedding: {embedding_result.get('error')}")
    else:
        print("HF_TOKEN not set. Skipping embedding example.")
