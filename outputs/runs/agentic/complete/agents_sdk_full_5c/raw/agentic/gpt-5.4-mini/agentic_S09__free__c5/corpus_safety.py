from embeddings_client import get_client, OPENAI_CHAT_MODEL


def corpus_safety(text: str):
    client = get_client()
    response = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You review text for safe embedding ingestion."},
            {"role": "user", "content": f"Check this corpus text for PII, secrets, or policy concerns: {text}"},
        ],
    )
    return {
        "provider": "openai",
        "model": OPENAI_CHAT_MODEL,
        "analysis": response.choices[0].message.content,
    }
