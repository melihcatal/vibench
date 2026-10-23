import os
import assemblyai as aai
from speech_models import TranscriptionRequest, TranscriptionResult, Word, Utterance

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


class SpeechClient:
    def __init__(self):
        self.transcriber = aai.Transcriber()

    def submit_transcription(
        self, request: TranscriptionRequest
    ) -> TranscriptionResult:
        config = aai.TranscriptionConfig(
            speaker_diarization=request.diarization,
            word_timestamps=request.word_timestamps,
            word_boost=["AssemblyAI"],
            auto_highlights=False,
            sentiment_analysis=False,
            iab_categories=False,
            content_safety=False,
        )
        transcript = self.transcriber.submit(request.audio_url, config=config)
        return TranscriptionResult(id=transcript.id, status=transcript.status)

    def poll_transcription(self, transcription_id: str) -> TranscriptionResult:
        transcript = self.transcriber.get_transcript_by_id(transcription_id)
        if transcript.status == aai.TranscriptStatus.completed:
            utterances = None
            if transcript.utterances:
                utterances = [
                    Utterance(
                        speaker=u.speaker,
                        text=u.text,
                        words=[
                            Word(text=w.text, start=w.start, end=w.end) for w in u.words
                        ],
                    )
                    for u in transcript.utterances
                ]
            return TranscriptionResult(
                id=transcript.id,
                status=transcript.status,
                text=transcript.text,
                utterances=utterances,
            )
        return TranscriptionResult(id=transcript.id, status=transcript.status)
