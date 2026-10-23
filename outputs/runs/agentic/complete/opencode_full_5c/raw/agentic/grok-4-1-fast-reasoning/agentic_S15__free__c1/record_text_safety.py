import os
from openai import OpenAI
from database_models import Document


def check_record_safety(record: Document) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = " ".join([str(v) for v in record["data"].values() if isinstance(v, str)])
    if not text:
        return {"flagged": False}
    response = client.moderations.create(input=text, model="text-moderation-latest")
    return response.results[0]
