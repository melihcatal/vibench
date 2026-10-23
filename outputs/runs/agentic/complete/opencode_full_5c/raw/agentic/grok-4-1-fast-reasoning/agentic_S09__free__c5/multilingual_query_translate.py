from embeddings_client import get_client


def translate_query_to_english(query: str) -> str:
    client = get_client()
    prompt = f"""Translate this search query to English precisely, preserving intent:

"{query}" """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()
