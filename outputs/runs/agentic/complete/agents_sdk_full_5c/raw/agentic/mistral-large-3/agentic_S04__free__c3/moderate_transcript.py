import os
from openai import OpenAI
from speech_models import ModerationRequest, ModerationResult

def moderate_transcript(request: ModerationRequest) -> ModerationResult:
    """Moderate transcript text before publishing using OpenAI Moderation API."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=request.text)
    result = response.results[0]
    return ModerationResult(
        flagged=result.flagged,
        categories={
            "hate": result.categories.hate,
            "hate/threatening": result.categories.hate_threatening,
            "self-harm": result.categories.self_harm,
            "sexual": result.categories.sexual,
            "sexual/minors": result.categories.sexual_minors,
            "violence": result.categories.violence,
            "violence/graphic": result.categories.violence_graphic,
        },
    )