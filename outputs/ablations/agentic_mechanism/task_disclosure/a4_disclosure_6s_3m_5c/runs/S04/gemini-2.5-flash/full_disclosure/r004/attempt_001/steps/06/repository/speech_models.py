import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class TranscriptionRequest:
    audio_file_uri: str
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = False
    enable_speaker_diarization: bool = False
    speaker_count: Optional[int] = None

@dataclasses.dataclass
class WordInfo:
    word: str
    start_time: float
    end_time: float
    speaker_tag: Optional[int] = None

@dataclasses.dataclass
class Segment:
    text: str
    start_time: float
    end_time: float
    speaker_tag: Optional[int] = None
    words: List[WordInfo] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class TranscriptionResult:
    transcript: str
    segments: List[Segment] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class TranscriptionResponse:
    job_id: str
    status: str
    result: Optional[TranscriptionResult] = None
    error: Optional[str] = None

def normalize_transcript(raw_transcript: dict) -> TranscriptionResult:
    """
    Normalizes a raw transcription result into a structured TranscriptionResult object.
    This is a placeholder function and would contain actual parsing logic based on
    the specific transcription service's response format.
    """
    full_transcript_text = ""
    segments = []

    # Example placeholder for parsing logic
    # In a real scenario, this would parse the 'raw_transcript' dictionary
    # based on the specific API response structure (e.g., Google Cloud Speech-to-Text, AWS Transcribe, etc.)
    # For now, let's assume a simple structure or just return an empty result.

    if "results" in raw_transcript and isinstance(raw_transcript["results"], list):
        for res in raw_transcript["results"]:
            if "alternatives" in res and isinstance(res["alternatives"], list) and res["alternatives"]:
                # Assuming the first alternative is the most confident
                alternative = res["alternatives"][0]
                if "transcript" in alternative:
                    full_transcript_text += alternative["transcript"] + " "

                if "words" in alternative and isinstance(alternative["words"], list):
                    current_segment_text = ""
                    current_segment_start = -1.0
                    current_segment_end = -1.0
                    segment_words = []
                    
                    for word_data in alternative["words"]:
                        word = word_data.get("word")
                        start_time = float(word_data.get("startTime", "0s").replace("s", ""))
                        end_time = float(word_data.get("endTime", "0s").replace("s", ""))
                        speaker_tag = word_data.get("speakerTag")

                        word_info = WordInfo(word=word, start_time=start_time, end_time=end_time, speaker_tag=speaker_tag)
                        segment_words.append(word_info)
                        
                        if current_segment_start == -1.0:
                            current_segment_start = start_time
                        current_segment_end = end_time
                        current_segment_text += word + " "
                    
                    if current_segment_text:
                        segments.append(Segment(
                            text=current_segment_text.strip(),
                            start_time=current_segment_start,
                            end_time=current_segment_end,
                            words=segment_words
                        ))
    
    return TranscriptionResult(
        transcript=full_transcript_text.strip(),
        segments=segments
    )
