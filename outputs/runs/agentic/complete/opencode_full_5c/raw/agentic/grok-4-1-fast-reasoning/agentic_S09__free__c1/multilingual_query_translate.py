import os
from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str = "English") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert translator. Translate the query accurately to the target language, preserving meaning for search purposes.",
            },
            {
                "role": "user",
                "content": f"Translate this search query to {target_language}: {query}",
            },
        ],
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()
