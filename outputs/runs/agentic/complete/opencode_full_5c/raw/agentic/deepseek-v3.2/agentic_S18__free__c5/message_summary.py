import os
from openai import OpenAI


def message_summary(messages, summary_length="short"):
    """Summarize message processing results using OpenAI GPT."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    if not messages:
        return {"summary": "No messages to summarize", "count": 0}

    message_texts = []
    for msg in messages:
        if isinstance(msg, dict):
            if "data" in msg and isinstance(msg["data"], dict):
                msg_text = str(msg["data"])
            else:
                msg_text = str(msg)
        else:
            msg_text = str(msg)
        message_texts.append(msg_text[:500])

    prompt = f"""Summarize these {len(messages)} processed messages in a {summary_length} summary:
    
    Messages:
    {" ".join(message_texts)}
    
    Provide a concise summary of the main themes, patterns, or issues found in these messages."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes message processing results.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200 if summary_length == "short" else 400,
        temperature=0.3,
    )

    summary = response.choices[0].message.content

    return {
        "summary": summary,
        "message_count": len(messages),
        "model_used": "gpt-3.5-turbo",
        "summary_length": summary_length,
    }
