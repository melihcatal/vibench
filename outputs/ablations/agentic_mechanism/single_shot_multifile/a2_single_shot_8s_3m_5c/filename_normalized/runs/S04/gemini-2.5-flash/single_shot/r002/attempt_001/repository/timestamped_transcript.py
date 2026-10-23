import json
import urllib.request
from speech_models import TranscriptionResult, TranscriptSegment, TranscriptWord

def get_timestamped_transcript(transcript_file_uri: str) -> TranscriptionResult:
    with urllib.request.urlopen(transcript_file_uri) as url:
        data = json.load(url)

    transcript_text = data["results"]["transcripts"][0]["transcript"]
    segments = []

    items = data["results"]["items"]
    speaker_labels = data["results"].get("speaker_labels", {}).get("segments", [])

    current_segment_words = []
    current_speaker = None
    current_segment_text_parts = []
    segment_start_time = None
    segment_end_time = None

    def get_speaker_at_time(time_val):
        if time_val is None: return None
        for sl in speaker_labels:
            if sl['start_time'] <= time_val < sl['end_time']:
                return sl['speaker_label']
        return None

    for i, item in enumerate(items):
        word_content = item.get("alternatives", [{}])[0].get("content")
        item_type = item.get("type")
        
        if item_type == 'pronunciation':
            start_time = float(item.get("start_time"))
            end_time = float(item.get("end_time"))
            speaker = get_speaker_at_time(start_time) if speaker_labels else None

            word = TranscriptWord(word=word_content, start_time=start_time, end_time=end_time, speaker_label=speaker)

            if not current_segment_words:
                segment_start_time = start_time
                current_speaker = speaker

            if current_segment_words and (current_speaker != speaker or (word_content in ['.', '?', '!'] and i < len(items) - 1 and items[i+1].get('type') == 'pronunciation')):
                segments.append(TranscriptSegment(
                    start_time=segment_start_time,
                    end_time=current_segment_words[-1].end_time,
                    speaker_label=current_speaker,
                    text="".join(current_segment_text_parts),
                    words=current_segment_words
                ))
                current_segment_words = []
                current_segment_text_parts = []
                segment_start_time = start_time
                current_speaker = speaker

            current_segment_words.append(word)
            current_segment_text_parts.append(word_content)
            segment_end_time = end_time
        
        elif item_type == 'punctuation' and current_segment_words:
            last_word = current_segment_words[-1]
            last_word.word += word_content
            if current_segment_text_parts:
                current_segment_text_parts[-1] += word_content
            
    if current_segment_words: # Add any remaining words as a final segment
        segments.append(TranscriptSegment(
            start_time=segment_start_time,
            end_time=segment_end_time if segment_end_time is not None else current_segment_words[-1].end_time,
            speaker_label=current_speaker,
            text="".join(current_segment_text_parts),
            words=current_segment_words
        ))

    return TranscriptionResult(
        job_name="N/A", # Job name not directly available from URI
        language_code=data["results"]["language_code"],
        transcript_text=transcript_text,
        segments=segments,
        raw_output=data
    )
