from openai import OpenAI
from typing import Optional, Dict
from pydantic import BaseModel
import os

class SummaryRequest(BaseModel):
    text: str
    model: str = "gpt-4o-mini"


class SummaryResponse(BaseModel):
    summary: Optional[str]
    error: Optional[str]

def archive_summary(text: str) -> SummaryResponse:
    """
    Summarizes transcription results using OpenAI Chat Completions API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize the following text:"},
                {"role": "user", "content": text},
            ],
            max_tokens=150,
        )
        return SummaryResponse(
            summary=response.choices[0].message.content.strip(),
            error=None
        )
    except Exception as e:
        return SummaryResponse(
            summary=None,
            error=str(e)
        )