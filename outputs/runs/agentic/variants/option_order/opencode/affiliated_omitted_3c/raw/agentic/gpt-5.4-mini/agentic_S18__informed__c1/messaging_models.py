from typing import Any, Dict, List, Optional


def normalize_message_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(payload)
    if "id" not in result:
        result["id"] = result.get("message_id", "msg")
    return result


def normalize_received_message(raw: Dict[str, Any], parsed: Dict[str, Any]) -> Dict[str, Any]:
    return {"message_id": raw.get("MessageId"), "receipt_handle": raw.get("ReceiptHandle"), "payload": parsed}


def build_publish_response(ok: bool, message_id: Optional[str] = None, error: Optional[str] = None, provider: str = "aws-sns") -> Dict[str, Any]:
    return {"ok": ok, "provider": provider, "message_id": message_id, "error": error}


def build_consume_response(ok: bool, message: Optional[Dict[str, Any]], provider: str = "aws-sqs") -> Dict[str, Any]:
    return {"ok": ok, "provider": provider, "message": message}


def build_dead_letter_response(ok: bool, message_id: Optional[str] = None, provider: str = "aws-sns") -> Dict[str, Any]:
    return {"ok": ok, "provider": provider, "message_id": message_id}


def build_batch_publish_response(ok: bool, results: List[Dict[str, Any]], provider: str = "aws-sns") -> Dict[str, Any]:
    return {"ok": ok, "provider": provider, "results": results}
