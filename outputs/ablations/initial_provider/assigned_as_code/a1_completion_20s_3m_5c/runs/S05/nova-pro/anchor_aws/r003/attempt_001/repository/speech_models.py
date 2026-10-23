from amazon_transcribe.model import TranscriptEvent, Result

def normalize_transcript_event(event):
    if isinstance(event, TranscriptEvent):
        results = [normalize_result(result) for result in event.transcript.results]
        return {'results': results}
    return event

def normalize_result(result):
    if isinstance(result, Result):
        alternatives = [{'transcript': alt.transcript, 'confidence': alt.confidence} for alt in result.alternatives]
        return {'alternatives': alternatives, 'is_partial': result.is_partial}
    return result