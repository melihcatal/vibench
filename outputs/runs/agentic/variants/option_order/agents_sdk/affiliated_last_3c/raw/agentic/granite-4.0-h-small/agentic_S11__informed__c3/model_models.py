from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class ModelInvocationRequest(BaseModel):
    deployment: str = Field(..., description="Provider-specific deployment ID or alias")
    model: Optional[str] = Field(None, description="Model identifier when not tied to a deployment")
    inference_profile: Optional[str] = Field(None, description="Inference profile or variant")
    prompt: str = Field(..., description="User prompt or input text")
    stream: bool = Field(False, description="Whether to stream output chunks")

class ModelInvocationResponse(BaseModel):
    text: str = Field(..., description="Generated textual output")
    request_id: Optional[str] = Field(None, description="Provider internal request identifier")
    model_handle: Optional[str] = Field(None, description="Exact model identifier used")
    usage: Optional[Dict[str, Any]] = Field(None, description="Usage metadata (tokens, price, etc.)")

class ModelResourceSpec(BaseModel):
    deployment: Optional[str] = Field(None, description="Deployment ID to use")
    model: Optional[str] = Field(None, description="Model identifier")
    inference_profile: Optional[str] = Field(None, description="Inference profile or variant")
