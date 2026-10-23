import os
from openai import OpenAI
from storage_models import SummaryResponse

def summarize_text(text_content: str, max_tokens: int = 150) -> SummaryResponse:
    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY')
    )
    model_id = "gpt-4o-mini"

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text_content}"}
        ],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    summary = response.choices[0].message.content.strip()
    return SummaryResponse(summary=summary)
