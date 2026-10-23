from speech_client import get_client, get_text_model


def translate_transcript(segments, target_language="en"):
    client = get_client()
    text = "\n".join(segment.get("text", "") for segment in segments)
    response = client.responses.create(
        model=get_text_model(),
        input=[
            {
                "role": "system",
                "content": "Translate transcript segments while preserving meaning and timestamps.",
            },
            {
                "role": "user",
                "content": f"Translate to {target_language}: {text}",
            },
        ],
    )
    return response.output_text
