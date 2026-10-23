from embeddings_client import get_embeddings_client

LLM_MODEL = "gpt-4o-mini"

def multilingual_query_translate(query: str, target_lang: str = "English") -> str:
    client = get_embeddings_client()
    prompt = f"""Translate this query to {target_lang}, respond ONLY with the translation:

{query}"""
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.1
    )
    return response.choices[0].message.content.strip()