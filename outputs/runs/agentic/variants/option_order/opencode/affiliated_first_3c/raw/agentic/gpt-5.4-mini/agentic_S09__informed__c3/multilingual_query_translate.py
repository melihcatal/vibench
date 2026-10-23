from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate the query faithfully and concisely."},
            {"role": "user", "content": f"Translate to {target_language}: {query}"},
        ],
    )
    return completion.choices[0].message.content
