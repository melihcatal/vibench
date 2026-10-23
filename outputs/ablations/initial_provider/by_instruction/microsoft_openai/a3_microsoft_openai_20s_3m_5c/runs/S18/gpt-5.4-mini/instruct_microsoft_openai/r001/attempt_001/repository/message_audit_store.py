import json
from pathlib import Path

from openai import OpenAI

from messaging_client import openai_endpoint, openai_model


def message_audit_store(record, path="message_audit.jsonl"):
    client = OpenAI(base_url=openai_endpoint())
    audit = {"record": record, "model": openai_model(), "provider": "openai", "verification": client.responses.create(model=openai_model(), input="Audit record validation").output_text}
    Path(path).write_text(json.dumps(audit) + "\n")
    return audit
