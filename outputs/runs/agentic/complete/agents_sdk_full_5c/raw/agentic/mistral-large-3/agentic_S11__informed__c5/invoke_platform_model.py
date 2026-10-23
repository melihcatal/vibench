from typing import Optional
import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import get_platform_config
from model_models import PlatformRequest, PlatformResponse

def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
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
    
    return PlatformResponse(
        output=response.text,
        metadata={
            "model_id": "gemini-1.5-pro-001",
            "usage": response.usage_metadata,
        }
    )