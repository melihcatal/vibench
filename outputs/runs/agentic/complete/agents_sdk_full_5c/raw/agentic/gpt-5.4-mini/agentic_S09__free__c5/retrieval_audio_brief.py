from embeddings_client import OPENAI_CHAT_MODEL, get_client


def retrieval_audio_brief(results):
    client = get_client()
    lines = []
    for idx, item in enumerate(results, start=1):
        lines.append(f"{idx}. {item.get('title', 'Untitled')}: {item.get('snippet', '')}")
    response = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[
            {"role": "system", "content": "Create a short spoken brief from retrieved search results."},
            {"role": "user", "content": "\n".join(lines)},
        ],
    )
    return {
        "provider": "openai",
        "model": OPENAI_CHAT_MODEL,
        "brief": response.choices[0].message.content,
    }
