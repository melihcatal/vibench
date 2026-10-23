import json
from typing import Any, Dict, List, Optional

# Define a simple request model for consistency
class PlatformModelRequest:
    def __init__(self, prompt: str,  
                 temperature: float = 0.7, 
                 max_output_tokens: int = 1024,
                 top_p: float = 0.8,
                 top_k: int = 40) -> None:
        self.prompt = prompt
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.top_p = top_p
        self.top_k = top_k

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
            "top_p": self.top_p,
            "top_k": self.top_k
        }

# Define a simple response model
class PlatformModelResponse:
    def __init__(self, text_output: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.text_output = text_output
        self.metadata = metadata if metadata is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text_output": self.text_output,
            "metadata": self.metadata
        }

    @classmethod
    def from_google_vertex_ai_response(cls, response: Any, model_id: str = "") -> 'PlatformModelResponse':
        """Normalizes a Google Cloud Vertex AI response into a standard format."""
        text_output = ""
        metadata = {}
        
        # This normalization is specific to the structure of Vertex AI's prediction response.
        if hasattr(response, 'predictions') and response.predictions:
            # Assuming the first prediction contains the text output
            prediction = response.predictions[0]
            if isinstance(prediction, dict) and "content" in prediction:
                text_output = prediction["content"]
            elif hasattr(prediction, "content"):
                 text_output = prediction.content
            elif isinstance(prediction, str):
                text_output = prediction


        # Collect metadata if available
        if hasattr(response, 'metadata'):
            metadata["vertex_ai_metadata"] = response.metadata
        
        # Add other useful info to metadata
        metadata["model_id"] = model_id
        
        return cls(text_output=text_output, metadata=metadata)

