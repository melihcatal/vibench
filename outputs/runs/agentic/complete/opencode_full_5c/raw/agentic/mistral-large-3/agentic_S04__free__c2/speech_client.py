from google.cloud import speech_v2 as speech
from google.cloud.speech_v2.types import cloud_speech
import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class TranscriptionConfig:
    project_id: str
    location: str
    recognizer_id: str
    model: str = "latest_long"
    language_codes: list[str] = None

    def __post_init__(self):
        if self.language_codes is None:
            self.language_codes = ["en-US"]


class SpeechClient:
    def __init__(self, config: TranscriptionConfig):
        self.config = config
        self.client = speech.SpeechClient()
        self.recognizer_path = f"projects/{config.project_id}/locations/{config.location}/recognizers/{config.recognizer_id}"

    def submit_transcription_job(self, audio_uri: str, job_name: str) -> str:
        recognition_config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=self.config.language_codes,
            model=self.config.model,
        )

        audio_source = cloud_speech.RecognitionAudio(uri=audio_uri)
        recognition_input = cloud_speech.RecognitionInput(audio=audio_source)

        request = cloud_speech.CreateRecognitionJobRequest(
            parent=self.recognizer_path,
            recognition_job=cloud_speech.RecognitionJob(
                name=job_name,
                recognition_config=recognition_config,
                input=recognition_input,
            ),
            recognition_job_id=job_name.split("/")[-1],
        )

        operation = self.client.create_recognition_job(request=request)
        operation.result()
        return f"{self.recognizer_path}/recognitionJobs/{job_name.split('/')[-1]}"

    def poll_transcription_job(self, job_path: str) -> cloud_speech.RecognitionResponse:
        request = cloud_speech.GetRecognitionJobRequest(name=job_path)
        return self.client.get_recognition_job(request=request)

    def enable_diarization(self, job_path: str, speaker_count: int) -> None:
        job = self.poll_transcription_job(job_path)
        if not job.recognition_config.features:
            job.recognition_config.features = cloud_speech.RecognitionFeatures()
        job.recognition_config.features.enable_speaker_diarization = True
        job.recognition_config.features.speaker_diarization_config = (
            cloud_speech.SpeakerDiarizationConfig(
                min_speaker_count=speaker_count, max_speaker_count=speaker_count
            )
        )

        request = cloud_speech.UpdateRecognitionJobRequest(
            recognition_job=job,
            update_mask={"paths": ["recognition_config"]},
        )
        self.client.update_recognition_job(request=request)

    def get_transcript_with_timestamps(
        self, job_path: str
    ) -> cloud_speech.RecognitionResponse:
        return self.poll_transcription_job(job_path)
