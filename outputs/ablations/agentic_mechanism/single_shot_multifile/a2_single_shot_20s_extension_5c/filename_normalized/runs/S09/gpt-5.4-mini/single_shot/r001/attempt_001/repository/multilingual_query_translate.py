import os
from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
    model = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")
    prompt = f"Translate the following query into {target_language} while preserving search intent and named entities: {query}"
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "You translate search queries."}, {"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()
