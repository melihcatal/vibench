import json
import os
from typing import Any, Dict, Iterable, List, Optional

import requests


SENDGRID_BATCH_CREATE_URL = "https://api.sendgrid.com/v3/mail/batch"
SENDGRID_MAIL_SEND_URL = "https://api.sendgrid.com/v3/mail/send"


def _sendgrid_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def create_sendgrid_batch_id(api_key: Optional[str] = None) -> str:
    api_key = api_key or os.environ["SENDGRID_API_KEY"]
    response = requests.post(
        SENDGRID_BATCH_CREATE_URL,
        headers=_sendgrid_headers(api_key),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    batch_id = data.get("batch_id")
    if not batch_id:
        raise RuntimeError("SendGrid did not return a batch_id")
    return batch_id


def build_sendgrid_message(
    to_email: str,
    subject: str,
    content: str,
    batch_id: str,
    custom_args: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    message: Dict[str, Any] = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": subject,
                "custom_args": custom_args or {},
            }
        ],
        "from": {"email": os.environ.get("SENDGRID_FROM_EMAIL", "noreply@example.com")},
        "content": [{"type": "text/plain", "value": content}],
        "batch_id": batch_id,
    }
    return message


def publish_batch_messages(
    messages: Iterable[Dict[str, Any]], api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    api_key = api_key or os.environ["SENDGRID_API_KEY"]
    results: List[Dict[str, Any]] = []
    for message in messages:
        response = requests.post(
            SENDGRID_MAIL_SEND_URL,
            headers=_sendgrid_headers(api_key),
            data=json.dumps(message),
            timeout=30,
        )
        results.append(
            {
                "status_code": response.status_code,
                "ok": response.ok,
                "response_text": response.text,
            }
        )
        response.raise_for_status()
    return results


def publish_batch_with_ids(
    recipients: Iterable[Dict[str, Any]],
    subject: str,
    content: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    batch_id = create_sendgrid_batch_id(api_key=api_key)
    messages = []
    for recipient in recipients:
        email = recipient["email"]
        attrs = {k: v for k, v in recipient.items() if k != "email"}
        messages.append(build_sendgrid_message(email, subject, content, batch_id, attrs))
    publish_results = publish_batch_messages(messages, api_key=api_key)
    return {"batch_id": batch_id, "results": publish_results}


if __name__ == "__main__":
    sample_recipients = [
        {"email": "alice@example.com", "id": "user-1", "segment": "alpha"},
        {"email": "bob@example.com", "id": "user-2", "segment": "beta"},
    ]
    output = publish_batch_with_ids(
        sample_recipients,
        subject="Batch publish example",
        content="This is a batched message.",
    )
    print(json.dumps(output, indent=2))
