import json


class TranscriptionJobResult:
    def __init__(self, raw_json):
        self._raw_json = raw_json

    @property
    def full_transcript(self):
        return self._raw_json["results"]["transcripts"][0]["transcript"]

    @property
    def items(self):
        return self._raw_json["results"]["items"]

    def get_timestamped_words(self):
        timestamped_words = []
        for item in self.items:
            if item["type"] == "pronunciation":
                timestamped_words.append({
                    "word": item["alternatives"][0]["content"],
                    "start_time": item["start_time"],
                    "end_time": item["end_time"],
                })
        return timestamped_words

    def get_diarized_segments(self):
        diarized_segments = []
        items = self.items
        
        current_speaker = None
        current_segment_text = ""
        current_start_time = None
        current_end_time = None

        for item in items:
            if item["type"] == "pronunciation":
                speaker_label = item.get("speaker_label")
                if speaker_label and speaker_label != current_speaker:
                    if current_segment_text:
                        diarized_segments.append({
                            "speaker": current_speaker,
                            "text": current_segment_text.strip(),
                            "start_time": current_start_time,
                            "end_time": current_end_time
                        })
                    current_speaker = speaker_label
                    current_segment_text = item["alternatives"][0]["content"]
                    current_start_time = item["start_time"]
                    current_end_time = item["end_time"]
                else:
                    current_segment_text += " " + item["alternatives"][0]["content"]
                    current_end_time = item["end_time"]
            elif item["type"] == "punctuation":
                current_segment_text += item["alternatives"][0]["content"]
                
        if current_segment_text:
            diarized_segments.append({
                "speaker": current_speaker,
                "text": current_segment_text.strip(),
                "start_time": current_start_time,
                "end_time": current_end_time
            })
        
        return diarized_segments

    @classmethod
    def from_uri(cls, uri):
        import urllib.request
        with urllib.request.urlopen(uri) as f:
            return cls(json.loads(f.read().decode("utf-8")))
