
class TranscriptionRequest:
    def __init__(self, audio_uri: str, language_code: str, speaker_count: int = None, enable_word_time_offsets: bool = False):
        self.audio_uri = audio_uri
        self.language_code = language_code
        self.speaker_count = speaker_count
        self.enable_word_time_offsets = enable_word_time_offsets

class TranscriptionResponse:
    def __init__(self, job_id: str, status: str, transcript: str = None, word_timestamps: list = None, diarization_result: list = None):
        self.job_id = job_id
        self.status = status
        self.transcript = transcript
        self.word_timestamps = word_timestamps
        self.diarization_result = diarization_result

    @staticmethod
    def from_operation(operation):
        return TranscriptionResponse(job_id=operation.operation.name, status="SUBMITTED")

    @staticmethod
    def from_completed_response(response):
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "

        word_timestamps = []
        diarization_result = []

        for result in response.results:
            for word_info in result.alternatives[0].words:
                word_timestamps.append({
                    "word": word_info.word,
                    "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                    "speaker_tag": word_info.speaker_tag if hasattr(word_info, 'speaker_tag') else None,
                })
            
            if hasattr(result.alternatives[0], 'words') and result.alternatives[0].words and hasattr(result.alternatives[0].words[0], 'speaker_tag'):
                # Simple diarization parsing for demonstration; more robust logic might be needed
                current_speaker = None
                current_segment_words = []
                for word_info in result.alternatives[0].words:
                    if current_speaker is None:
                        current_speaker = word_info.speaker_tag
                        current_segment_words = [word_info.word]
                    elif current_speaker == word_info.speaker_tag:
                        current_segment_words.append(word_info.word)
                    else:
                        diarization_result.append({
                            "speaker": current_speaker,
                            "segment": " ".join(current_segment_words),
                            "start_time": word_timestamps[-len(current_segment_words)]["start_time"],
                            "end_time": word_timestamps[-1]["end_time"],
                        })
                        current_speaker = word_info.speaker_tag
                        current_segment_words = [word_info.word]
                if current_segment_words:
                    diarization_result.append({
                        "speaker": current_speaker,
                        "segment": " ".join(current_segment_words),
                        "start_time": word_timestamps[-len(current_segment_words)]["start_time"],
                        "end_time": word_timestamps[-1]["end_time"],
                    })


        return TranscriptionResponse(
            job_id=None, # Not relevant for a completed response directly
            status="COMPLETED",
            transcript=transcript.strip(),
            word_timestamps=word_timestamps,
            diarization_result=diarization_result,
        )
