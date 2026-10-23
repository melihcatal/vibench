from google.cloud import speech_v2

from speech_client import default_output_uri, load_config


def diarized_transcript(audio_uri: str):
    config = load_config()
    client = speech_v2.SpeechClient()
    request = speech_v2.BatchRecognizeRequest(
        recognizer=f"projects/{config.project_id}/locations/{config.location}/recognizers/_",
        files=[speech_v2.BatchRecognizeFileMetadata(uri=audio_uri)],
        recognition_config=speech_v2.RecognitionConfig(
            auto_decoding_config=speech_v2.AutoDetectDecodingConfig(),
            features=speech_v2.RecognitionFeatures(enable_speaker_diarization=True),
            model="chirp_2",
        ),
        output_config=speech_v2.BatchRecognizeOutputConfig(gcs_output_config=speech_v2.GcsOutputConfig(uri=default_output_uri(config, "transcriptions/diarized"))),
    )
    return client.batch_recognize(request=request).operation.name
