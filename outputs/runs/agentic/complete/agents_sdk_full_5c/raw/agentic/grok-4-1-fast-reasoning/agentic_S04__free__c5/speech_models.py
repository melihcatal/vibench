from typing import Dict, Any, List, Optional, TypedDict

class TimestampedWord(TypedDict, total=False):
    start_time: str
    end_time: str
    word: str
    confidence: Optional[float]

class DiarizedSegment(TypedDict, total=False):
    start_time: str
    end_time: str
    speaker_label: Optional[str]
    channel_label: Optional[str]
    text: str

def extract_transcript(results: Dict[str, Any]) -> str:
    if 'results' not in results or not results['results']['transcripts']:
        return ''
    return results['results']['transcripts'][0]['transcript']

def extract_words(results: Dict[str, Any]) -> List[TimestampedWord]:
    words = []
    if 'results' not in results or 'items' not in results['results']:
        return words
    for item in results['results']['items']:
        if item['type'] == 'pronunciation':
            alt = item['alternatives'][0]
            word_data: TimestampedWord = {
                'start_time': item['start_time'],
                'end_time': item['end_time'],
                'word': alt['content'],
                'confidence': alt.get('confidence')
            }
            words.append(word_data)
    return words

def extract_segments(results: Dict[str, Any]) -> List[DiarizedSegment]:
    segments = []
    if 'results' not in results or 'items' not in results['results']:
        return segments
    for item in results['results']['items']:
        if item['type'] == 'pronunciation':
            alt = item['alternatives'][0]
            seg: DiarizedSegment = {
                'start_time': item['start_time'],
                'end_time': item['end_time'],
                'speaker_label': alt.get('speaker_label'),
                'channel_label': item.get('channel_label'),
                'text': alt['content']
            }
            segments.append(seg)
    return segments