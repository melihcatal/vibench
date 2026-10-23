from typing import TypedDict, Any, Tuple

class DeepgramTranscript(TypedDict, total=False):
    type: str
    channel: dict[str, Any]
    is_final: bool

def extract_transcript(transcript: DeepgramTranscript) -> Tuple[str, bool]:
    if 'channel' in transcript and 'alternatives' in transcript['channel'] and transcript['channel']['alternatives']:
        alt = transcript['channel']['alternatives'][0]
        text = alt.get('transcript', '')
        is_final = transcript.get('is_final', False)
        return text, is_final
    return '', False