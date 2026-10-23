from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    model_id: str = Field(
        "granite-4.0-h-small", description="Model identifier for inference"
    )
    inputs: str = Field(..., description="Prompt or text to process")
    parameters: dict = Field({"temperature": 0.7}, description="Inference parameters")


class LLMResponse(BaseModel):
    generated_text: str = Field(..., description="Model-generated output")
    usage: dict = Field(None, description="Optional usage metrics")


class Normalizer:
    @staticmethod
    def to_dict(response_obj):
        # Convert Pydantic model to plain dict for downstream use
        return response_obj.dict()


if __name__ == "__main__":
    req = LLMRequest(inputs="Hello world")
    print("Request model:", req)
    print("Normalized:", Normalizer.to_dict(req))
