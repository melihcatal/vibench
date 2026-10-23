import os
import openai
from identity_models import SummaryRequest

def summarize_onboarding_state(request: SummaryRequest) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
            {"role": "user", "content": f"Summarize the following text: {request.text}"}
        ],
        max_tokens=request.max_tokens,
        temperature=0.7,
    )

    if response.choices:
        return response.choices[0].message.content.strip()
    return "" # Return empty string if no summary generated
