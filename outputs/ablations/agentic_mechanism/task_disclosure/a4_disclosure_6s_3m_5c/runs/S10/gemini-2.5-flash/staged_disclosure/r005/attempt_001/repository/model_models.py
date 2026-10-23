import dataclasses
from typing import Any, Dict, List, Optional, Union

@dataclasses.dataclass
class ModelRequest:
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7
    top_p: float = 1.0
    stop_sequences: Optional[List[str]] = None
    model_family: Optional[str] = None # For model family selection

@dataclasses.dataclass
class ModelResponse:
    text: str
    model_family: Optional[str] = None
    
def normalize_request(input_data: Dict[str, Any]) -> ModelRequest:
    """
    Normalizes a dictionary of input data into a ModelRequest object.
    This helper can handle various input formats and map them to our standardized ModelRequest.
    """
    prompt = input_data.get("prompt") or input_data.get("text")
    if not prompt:
        raise ValueError("Prompt or text must be provided in the input data.")
    
    return ModelRequest(
        prompt=prompt,
        max_tokens=input_data.get("max_tokens", 100),
        temperature=input_data.get("temperature", 0.7),
        top_p=input_data.get("top_p", 1.0),
        stop_sequences=input_data.get("stop_sequences"),
        model_family=input_data.get("model_family")
    )

def normalize_response(llm_output: Dict[str, Any], model_family: Optional[str] = None) -> ModelResponse:
    """
    Normalizes the output from an LLM inference into a standardized ModelResponse object.
    This helper can extract the relevant text from different LLM provider response structures.
    """
    text = llm_output.get("generated_text") or llm_output.get("text") or llm_output.get("choices", [{}])[0].get("text")
    if not text:
        raise ValueError("Could not extract text from LLM output.")
        
    return ModelResponse(
        text=text,
        model_family=model_family
    )
