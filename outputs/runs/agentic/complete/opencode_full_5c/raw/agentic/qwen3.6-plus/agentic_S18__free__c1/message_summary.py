import os
import time
from typing import Optional

import openai

from messaging_models import MessageSummary, EventMessage, extract_text_from_payload

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"


def summarize_message(
    event: EventMessage,
    max_words: int = 50,
    model: str = OPENAI_MODEL,
) -> MessageSummary:
    text = extract_text_from_payload(event.payload)
    start_time = time.time()

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a message summarization assistant. "
                    "Provide a concise summary, extract key topics, and detect sentiment."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Summarize the following message in {max_words} words or fewer. "
                    f"Also identify key topics and sentiment (positive, negative, or neutral).\n\n"
                    f"Message: {text}"
                ),
            },
        ],
        temperature=0.3,
        max_tokens=256,
    )

    processing_time_ms = (time.time() - start_time) * 1000
    summary_text = response.choices[0].message.content.strip()

    topic_response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Extract 3-5 key topic keywords from the text. Return only a comma-separated list.",
            },
            {
                "role": "user",
                "content": f"Text: {text}",
            },
        ],
        temperature=0.2,
        max_tokens=64,
    )

    key_topics = [
        t.strip()
        for t in topic_response.choices[0].message.content.strip().split(",")
        if t.strip()
    ]

    sentiment_response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Classify the sentiment as positive, negative, or neutral. Return only the word.",
            },
            {
                "role": "user",
                "content": f"Text: {text}",
            },
        ],
        temperature=0.1,
        max_tokens=16,
    )

    sentiment = sentiment_response.choices[0].message.content.strip().lower()
    word_count = len(summary_text.split())

    return MessageSummary(
        message_id=event.event_id,
        summary_text=summary_text,
        key_topics=key_topics,
        sentiment=sentiment,
        word_count=word_count,
        processing_time_ms=round(processing_time_ms, 2),
    )


def summarize_message_text(
    text: str,
    message_id: str = "",
    max_words: int = 50,
    model: str = OPENAI_MODEL,
) -> MessageSummary:
    event = EventMessage(
        event_id=message_id,
        payload={"text": text},
    )
    return summarize_message(event, max_words=max_words, model=model)
