from typing import Dict, Any, List

def normalize_bedrock_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes AWS Bedrock response into a common format.
    """
    # Assuming the response body contains a 'completion' field for text.
    # More complex parsing might be needed depending on the model and response structure.
    return {"text": response.get("completion", ""), "raw_response": response}

def normalize_azure_openai_stream_chunk(chunk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes Azure OpenAI stream chunk.
    """
    if 'choices' in chunk and chunk['choices']:
        text = chunk['choices'][0].get('text', '')
        return {"text": text, "raw_chunk": chunk}
    return {"text": "", "raw_chunk": chunk}

def normalize_cohere_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes Cohere response.
    """
    text = response.get("text", "")
    metadata = {k: v for k, v in response.items() if k != "text"}
    return {"text": text, "metadata": metadata, "raw_response": response}

def create_vertex_ai_prediction_request(prompt: str) -> Dict[str, Any]:
    """
    Creates a generic request payload for Vertex AI predictions.
    This will vary greatly depending on the specific model deployed.
    """
    # Example for a text-bison model
    return {
        "instances": [{
            "prompt": prompt
        }],
        "parameters": {
            "temperature": 0.2,
            "maxOutputTokens": 256,
            "topP": 0.95,
            "topK": 40
        }
    }
