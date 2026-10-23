def normalize_job(payload):
    if isinstance(payload, dict):
        return {
            'id': payload.get('self') or payload.get('id') or payload.get('jobId'),
            'status': payload.get('status'),
            'locale': payload.get('locale') or payload.get('language'),
            'raw': payload,
        }
    return {'id': None, 'status': None, 'locale': None, 'raw': payload}


def normalize_transcription(payload):
    values = payload.get('values') if isinstance(payload, dict) else None
    if values is None and isinstance(payload, dict):
        values = payload.get('combinedRecognizedPhrases') or payload.get('recognizedPhrases') or payload.get('phrases') or []
    return values or []


def flatten_segments(result):
    segments = []
    for item in normalize_transcription(result):
        if isinstance(item, dict):
            text = item.get('display') or item.get('nBest', [{}])[0].get('display') or item.get('text') or ''
            speaker = item.get('speaker') or item.get('speakerNumber')
            offset = item.get('offsetInTicks') or item.get('offset')
            duration = item.get('durationInTicks') or item.get('duration')
            words = item.get('words') or []
            segments.append({'text': text, 'speaker': speaker, 'offset': offset, 'duration': duration, 'words': words, 'raw': item})
    return segments
