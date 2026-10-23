def normalize_segments(segments):
    return [{'start': s.get('start'), 'end': s.get('end'), 'text': s.get('text', '').strip()} for s in segments or []]


def normalize_transcript(response):
    if isinstance(response, dict):
        return {
            'job_id': response.get('self') or response.get('job_id'),
            'status': response.get('status'),
            'text': response.get('combinedRecognizedPhrases', response.get('text', '')),
            'segments': normalize_segments(response.get('segments') or response.get('recognizedPhrases')),
        }
    return {'job_id': None, 'status': None, 'text': response, 'segments': []}
