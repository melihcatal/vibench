import os
from openai import OpenAI
from translation_models import TextToSummarize, SummaryResponse

def summarize_translation_quality(request: TextToSummarize) -> SummaryResponse:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes translation quality issues."},
            {"role": "user", "content": f"Summarize any quality issues in the following translated text: {request.text}"}
        ]
    )

    summary = response.choices[0].message.content
    return SummaryResponse(summary=summary)
