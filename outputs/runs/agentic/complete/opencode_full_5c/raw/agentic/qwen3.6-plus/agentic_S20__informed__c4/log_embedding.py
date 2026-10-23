import os

import openai

from fetch_recent_logs import fetch_recent_logs
from observability_models import NormalizedLogEntry


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def extract_log_messages_for_embedding(log_entries):
    messages = []
    for entry in log_entries:
        if isinstance(entry, dict):
            msg = entry.get("message", "")
        elif isinstance(entry, NormalizedLogEntry):
            msg = entry.message
        else:
            msg = str(entry)
        if msg:
            messages.append(msg)
    return messages


def generate_embeddings(
    messages,
    model=None,
    field_filters=None,
    time_from=None,
    time_to=None,
    limit=50,
):
    embed_model = model or OPENAI_EMBEDDING_MODEL

    if isinstance(messages, list) and len(messages) > 0:
        log_messages = messages
    else:
        raw_response = fetch_recent_logs(
            field_filters=field_filters,
            time_from=time_from,
            time_to=time_to,
            limit=limit,
        )
        data = raw_response.get("data", [])
        entries = [NormalizedLogEntry.from_datadog_event(evt) for evt in data]
        log_messages = extract_log_messages_for_embedding(entries)

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        model=embed_model,
        input=log_messages,
    )

    embeddings = []
    for item in response.data:
        embeddings.append(
            {
                "index": item.index,
                "embedding": item.embedding,
                "message": log_messages[item.index]
                if item.index < len(log_messages)
                else "",
            }
        )

    return embeddings


def log_embedding(
    messages=None,
    model=None,
    field_filters=None,
    time_from=None,
    time_to=None,
    limit=50,
):
    return generate_embeddings(
        messages=messages,
        model=model,
        field_filters=field_filters,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
    )
