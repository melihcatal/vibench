import os
from typing import Optional
from openai import OpenAI
from storage_models import SummaryRequest, SummaryResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def summarize_stored_asset(request: SummaryRequest) -> SummaryResponse:
    if not request.text or not request.text.strip():
        return SummaryResponse(
            success=False,
            model_used=request.model,
            error_message="Input text is empty",
        )

    if not OPENAI_API_KEY:
        return SummaryResponse(
            success=False,
            model_used=request.model,
            error_message="OPENAI_API_KEY environment variable is not set",
        )

    client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt = (
        "You are a helpful assistant that summarizes documents and assets concisely."
    )

    if request.focus:
        system_prompt = (
            f"You are a helpful assistant that summarizes documents and assets. "
            f"Focus your summary on: {request.focus}"
        )

    user_prompt = (
        f"Please summarize the following content in a clear and concise manner. "
        f"Keep the summary under {request.max_tokens} tokens.\n\n"
        f"{request.text}"
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        summary = completion.choices[0].message.content or ""
        tokens_used = completion.usage.total_tokens if completion.usage else None

        return SummaryResponse(
            success=True,
            summary=summary,
            model_used="gpt-4o",
            tokens_used=tokens_used,
        )
    except Exception as e:
        return SummaryResponse(
            success=False,
            model_used="gpt-4o",
            error_message=f"OpenAI gpt-4o summarization failed: {str(e)}",
        )


def summarize_asset_text(
    text: str, max_tokens: int = 500, focus: Optional[str] = None
) -> SummaryResponse:
    request = SummaryRequest(
        text=text,
        max_tokens=max_tokens,
        focus=focus,
        model="gpt-4o",
    )
    return summarize_stored_asset(request)
