from __future__ import annotations

from typing import Any

from messaging_client import send_to_dead_letter


def dead_letter_message(
    message_id: str,
    payload: dict[str, Any],
    reason: str,
    attributes: dict[str, str] | None = None,
) -> dict[str, str]:
    response = send_to_dead_letter(
        {
            "failed_message_id": message_id,
            "reason": reason,
            "payload": payload,
        },
        attributes=attributes,
    )
    return {
        "dead_letter_message_id": response["MessageId"],
        "sequence_number": response.get("SequenceNumber", ""),
    }
