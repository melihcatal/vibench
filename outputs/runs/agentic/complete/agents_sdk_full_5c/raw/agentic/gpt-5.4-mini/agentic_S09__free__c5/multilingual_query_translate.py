from embeddings_client import get_client, OPENAI_CHAT_MODEL


def multilingual_query_translate(query: str, target_language: str = "English"):
    client = get_client()
    response = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You translate search queries for multilingual retrieval."},
            {"role": "user", "content": f"Translate the query into {target_language} while preserving meaning: {query}"},
        ],
    )
    return response.choices[0].message.content
