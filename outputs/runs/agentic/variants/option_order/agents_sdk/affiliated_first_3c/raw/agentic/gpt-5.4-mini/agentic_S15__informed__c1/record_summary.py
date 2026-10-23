from openai import OpenAI

from database_models import DocumentResponse

MODEL_ID = "gpt-4o-mini"


def summarize_record(record: dict) -> DocumentResponse:
    client = OpenAI()
    prompt = f"Summarize this managed NoSQL document in one concise paragraph:\n{record}"
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize document records."},
            {"role": "user", "content": prompt},
        ],
    )
    text = completion.choices[0].message.content if completion.choices else ""
    return DocumentResponse(ok=True, data={"summary": text})
