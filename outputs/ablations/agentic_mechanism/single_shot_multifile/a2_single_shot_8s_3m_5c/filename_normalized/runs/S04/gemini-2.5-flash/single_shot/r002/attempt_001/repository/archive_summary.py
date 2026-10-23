from speech_client import get_openai_client
from speech_models import SummaryResult

def summarize_transcript(text: str, model: str = "gpt-3.5-turbo") -> SummaryResult:
    client = get_openai_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts concisely."},
            {"role": "user", "content": f"Please summarize the following transcript:\n\n{text}"}
        ],
        max_tokens=200
    )

    summary = response.choices[0].message.content.strip()

    return SummaryResult(
        original_text=text,
        summary_text=summary,
        model_used=model
    )
