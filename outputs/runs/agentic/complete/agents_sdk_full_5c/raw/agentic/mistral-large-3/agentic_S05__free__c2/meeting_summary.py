from openai import OpenAI
from speech_models import FinalResult

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_transcript(results: list[FinalResult], model: str = "gpt-4o-mini") -> str:
    transcript = " ".join([result.transcript for result in results])
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize the following meeting transcript."},
            {"role": "user", "content": transcript},
        ],
    )
    return response.choices[0].message.content