from google.cloud import speech_v1p1beta1 as speech

def diarize_transcript(audio_uri: str):
    """
    Requests speaker diarization for a recorded meeting using Google Cloud Speech-to-Text.

    Args:
        audio_uri (str): The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").

    Returns:
        google.cloud.speech_v1p1beta1.types.LongRunningRecognizeResponse: The response containing the diarized transcript.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2,  # Specify the number of speakers if known
        # You can adjust min and max speaker counts for better accuracy
        # diarization_config=speech.SpeakerDiarizationConfig(
        #     min_speaker_count=2,
        #     max_speaker_count=4,
        # )
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # The response will contain results with speaker tags
    return response

if __name__ == "__main__":
    # Example usage (replace with your actual audio URI)
    # Ensure you have authenticated with Google Cloud, e.g., using `gcloud auth application-default login`
    # and enabled the Speech-to-Text API in your Google Cloud project.
    
    # For a real application, you would typically pass the audio_uri dynamically.
    # This example uses a placeholder URI; replace it with a valid Google Cloud Storage URI
    # to an audio file.
    example_audio_uri = "gs://cloud-samples-data/speech/corvair.flac" 
    
    try:
        print(f"Submitting for diarization: {example_audio_uri}")
        diarization_response = diarize_transcript(example_audio_uri)
        
        print("Diarization complete. Transcript:")
        for result in diarization_response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")
            for word_info in result.alternatives[0].words:
                print(f"Word: {word_info.word}, Speaker: {word_info.speaker_tag}")
                
    except Exception as e:
        print(f"An error occurred: {e}")
