from typing import Dict, Any
import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import get_platform_config
from model_models import PlatformRequest, PlatformResponse

def collect_platform_metadata(request: PlatformRequest) -> Dict[str, Any]:
    config = get_platform_config()
    vertexai.init(project=config["project_id"], location=config["location"])
    model = GenerativeModel(model_name="gemini-1.5-pro-001")
    
    response = model.generate_content(
        contents=request.prompt,
        generation_config={
            "max_output_tokens": request.max_tokens,
            "temperature": request.temperature,
        }
    )
    
    return {
        "output": response.text,
        "metadata": {
            "model_id": "gemini-1.5-pro-001",
            "usage": {
                "prompt_token_count": response.usage_metadata.prompt_token_count,
                "candidates_token_count": response.usage_metadata.candidates_token_count,
                "total_token_count": response.usage_metadata.total_token_count,
            },
            "finish_reason": response.candidates[0].finish_reason.name,
        }
    }