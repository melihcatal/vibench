import os
from typing import Optional
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
from messaging_models import EventMessage, AuditRecord


GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "default-project")
GCP_LOCATION = os.environ.get("VERTEX_AI_LOCATION", "us-central1")
SUMMARY_MODEL_ID = "gemini-1.5-flash-001"


def initialize_vertex_ai():
    aiplatform.init(
        project=GCP_PROJECT_ID,
        location=GCP_LOCATION,
    )


def summarize_processing_results(
    processed_messages: list, summary_prompt: str = None
) -> str:
    initialize_vertex_ai()
    model = GenerativeModel(SUMMARY_MODEL_ID)

    message_summaries = []
    for msg in processed_messages:
        if isinstance(msg, AuditRecord):
            message_summaries.append(
                f"Event {msg.event_id} ({msg.event_type}): status={msg.status}, result={msg.processing_result}"
            )
        elif isinstance(msg, dict):
            message_summaries.append(
                f"Event {msg.get('event_id', 'unknown')} ({msg.get('event_type', 'unknown')}): status={msg.get('status', 'unknown')}"
            )
        elif isinstance(msg, EventMessage):
            message_summaries.append(
                f"Event {msg.event_id} ({msg.event_type}): payload_keys={list(msg.payload.keys())}"
            )

    messages_text = "\n".join(message_summaries)

    default_prompt = (
        f"Summarize the following message processing results. "
        f"Provide a concise overview including total count, success/failure breakdown, "
        f"and any notable patterns or issues:\n\n{messages_text}"
    )

    prompt = summary_prompt or default_prompt

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as exc:
        return f"Summary generation failed: {str(exc)}"


def summarize_single_message(event_data: dict) -> str:
    initialize_vertex_ai()
    model = GenerativeModel(SUMMARY_MODEL_ID)

    event = EventMessage.from_dict(event_data)
    prompt = (
        f"Summarize this event in one sentence:\n"
        f"Type: {event.event_type}\n"
        f"Source: {event.source}\n"
        f"Payload: {event.payload}"
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as exc:
        return f"Summary failed: {str(exc)}"
