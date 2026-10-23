from typing import Dict, List, Optional

class TranscriptionJobRequest:
    def __init__(self, audio_uri: str, job_name: str, language_code: str, media_format: str, output_bucket: Optional[str] = None, show_speaker_labels: bool = False, max_speaker_labels: int = 2):
        self.audio_uri = audio_uri
        self.job_name = job_name
        self.language_code = language_code
        self.media_format = media_format
        self.output_bucket = output_bucket
        self.show_speaker_labels = show_speaker_labels
        self.max_speaker_labels = max_speaker_labels

    def to_aws_params(self) -> Dict:
        params = {
            'TranscriptionJobName': self.job_name,
            'LanguageCode': self.language_code,
            'MediaFormat': self.media_format,
            'Media': {'MediaFileUri': self.audio_uri}
        }
        if self.output_bucket:
            params['OutputBucketName'] = self.output_bucket
        if self.show_speaker_labels:
            params['Settings'] = {
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': self.max_speaker_labels
            }
        return params

class TranscriptionSegment:
    def __init__(self, text: str, start_time: Optional[float] = None, end_time: Optional[float] = None, speaker_label: Optional[str] = None):
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.speaker_label = speaker_label

    def to_dict(self) -> Dict:
        return {
            'text': self.text,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'speaker_label': self.speaker_label
        }

def parse_aws_transcript_result(transcript_json: Dict) -> List[TranscriptionSegment]:
    segments = []
    # This parsing is simplified; real AWS Transcribe output can be complex
    # For speaker diarization, often need to reconstruct segments from items and speaker labels
    
    # Simple approach for overall transcript
    if 'results' in transcript_json and 'transcripts' in transcript_json['results'] and transcript_json['results']['transcripts']:
        full_text = transcript_json['results']['transcripts'][0]['transcript']
        segments.append(TranscriptionSegment(text=full_text))

    # For word/item level timestamps and speaker labels
    if 'results' in transcript_json and 'items' in transcript_json['results']:
        current_segment_text = []
        current_segment_start = None
        current_segment_end = None
        current_speaker = None

        for item in transcript_json['results']['items']:
            content = item['alternatives'][0]['content']
            item_type = item['type']
            speaker_label = item.get('speaker_label')
            start_time = float(item.get('start_time')) if 'start_time' in item else None
            end_time = float(item.get('end_time')) if 'end_time' in item else None

            if item_type == 'pronunciation':
                if current_speaker is None:
                    current_speaker = speaker_label

                if speaker_label != current_speaker or (not speaker_label and not current_speaker):
                    if current_segment_text:
                        segments.append(TranscriptionSegment(
                            text=' '.join(current_segment_text),
                            start_time=current_segment_start,
                            end_time=current_segment_end,
                            speaker_label=current_speaker
                        ))
                    current_segment_text = [content]
                    current_segment_start = start_time
                    current_segment_end = end_time
                    current_speaker = speaker_label
                else:
                    current_segment_text.append(content)
                    if current_segment_start is None: current_segment_start = start_time
                    current_segment_end = end_time

        if current_segment_text:
            segments.append(TranscriptionSegment(
                text=' '.join(current_segment_text),
                start_time=current_segment_start,
                end_time=current_segment_end,
                speaker_label=current_speaker
            ))

    return segments
