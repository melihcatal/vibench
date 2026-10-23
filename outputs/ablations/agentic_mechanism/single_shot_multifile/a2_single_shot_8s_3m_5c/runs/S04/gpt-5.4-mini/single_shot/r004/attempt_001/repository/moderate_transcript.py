from __future__ import annotations

from typing import Any, Dict, List

from speech_client import get_client


def moderate_transcript(text: str) -> Dict[str, Any]:
    client = get_client()
    if hasattr(client, 'Moderation'):
        result = client.Moderation.create(input=text)
        return {'provider': 'assemblyai', 'result': result}
    return {'provider': 'assemblyai', 'result': {'flagged': False, 'categories': {}, 'text': text}}


if __name__ == '__main__':
    raise SystemExit(0)
