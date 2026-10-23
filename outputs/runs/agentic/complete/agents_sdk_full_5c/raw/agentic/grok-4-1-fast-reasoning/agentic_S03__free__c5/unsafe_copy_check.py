import os
from openai import OpenAI

def check_unsafe_content(text: str) -> dict[str, bool]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        input=text,
        model="text-moderation-latest",
    )
    result = response.results[0]
    return dict(result.categories)
