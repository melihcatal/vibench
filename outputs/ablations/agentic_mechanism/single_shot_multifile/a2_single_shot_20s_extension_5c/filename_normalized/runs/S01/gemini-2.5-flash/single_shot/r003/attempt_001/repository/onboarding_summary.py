import os
import openai
from identity_client import get_openai_api_key
from identity_models import SummarizeRequest, SummarizeResponse

def onboarding_summary(request: SummarizeRequest) -> SummarizeResponse:
    api_key = get_openai_api_key()
    client = openai.OpenAI(api_key=api_key)

    prompt_text = (
        f"Context: {request['context']}\n\n"
        f"Summarize the following onboarding state for a support agent: {request['text']}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes user onboarding states for support personnel."},
            {"role": "user", "content": prompt_text}
        ],
        max_tokens=150
    )

    summary = response.choices[0].message.content.strip() if response.choices else ""
    return {"summary": summary}