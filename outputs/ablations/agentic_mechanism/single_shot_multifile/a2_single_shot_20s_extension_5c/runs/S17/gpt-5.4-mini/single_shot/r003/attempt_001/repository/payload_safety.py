from __future__ import annotations

from typing import Any, Dict

from google.cloud import contentmoderator_v1


def payload_safety(decrypted_text: str) -> Dict[str, Any]:
    client = contentmoderator_v1.ContentModeratorClient()
    response = client.screen_text(request={"text_content": decrypted_text, "language": "eng"})
    unsafe = any(getattr(item, "category_name", "") for item in getattr(response, "classification", []))
    return {"unsafe": unsafe, "raw_response": response.__class__.__name__}
