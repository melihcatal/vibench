import os
from pydantic import BaseModel
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


class ModerationRequest(BaseModel):
    text: str


class ModerationResponse(BaseModel):
    is_flagged: bool
    categories: dict


def moderate_profile_text(request: ModerationRequest) -> ModerationResponse:
    response = client.moderations.create(input=request.text)
    result = response.results[0]
    
    return ModerationResponse(
        is_flagged=result.flagged,
        categories=result.categories.model_dump(),
    )