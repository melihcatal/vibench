from typing import List, Dict, Any

# A simplified model for an embedding response structure.
# This helper would typically normalize responses from a specific provider.
# For OpenAI, the SDK client directly returns convenient objects.
def normalize_embedding_response(response_data: Dict[str, Any]) -> List[List[float]]:
    # Example: If needing to parse a raw HTTP response or a different SDK format
    # For OpenAI's Python SDK, response.data[i].embedding already gives the list of floats.
    # This function is a placeholder for potential normalization if needed.
    embeddings = []
    if "data" in response_data and isinstance(response_data["data"], list):
        for item in response_data["data"]:
            if "embedding" in item and isinstance(item["embedding"], list):
                embeddings.append(item["embedding"])
    return embeddings
