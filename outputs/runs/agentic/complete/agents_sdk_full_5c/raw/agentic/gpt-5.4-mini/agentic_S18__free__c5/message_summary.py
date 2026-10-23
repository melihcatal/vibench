import json
import sys
from typing import Any, Dict

from google.cloud import language_v1

from messaging_models import ProcessingRecord, now_iso


client = language_v1.LanguageServiceClient()


def summarize_message(message: Dict[str, Any]) -> ProcessingRecord:
    text = json.dumps(message, ensure_ascii=False, sort_keys=True)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document})
    summary = f"score={sentiment.document_sentiment.score:.3f}; magnitude={sentiment.document_sentiment.magnitude:.3f}"
    return ProcessingRecord(message_id=str(message.get("message_id") or message.get("id") or "unknown"), status="summarized", summary=summary, processed_at=now_iso(), metadata={"provider": "google-cloud-language"})


if __name__ == "__main__":
    raw = sys.stdin.read().strip() or "{}"
    message = json.loads(raw)
    record = summarize_message(message)
    print(json.dumps({"message_id": record.message_id, "status": record.status, "summary": record.summary, "processed_at": record.processed_at, "metadata": record.metadata}, ensure_ascii=False))
