from google.cloud import speech_v1p1beta1 as speech

def handle_streaming_transcription_events(responses):
    for response in responses:
        if not response.results:
            continue

        # The `results` list contains consecutive `SpeechRecognitionResult` objects.
        # The top result has primary transcript and confidence along with 'is_final'.
        result = response.results[0]
        if not result.alternatives:
            continue

        # The `alternatives` list provides the top N hypotheses for the utterance
        # being processed. Only the first alternative is typically needed for
        # streaming.
        transcript = result.alternatives[0].transcript

        if result.is_final:
            print(f"Final transcript: {transcript}")
            # You can send this final transcript to other services (e.g., translation, safety)
            yield {'type': 'final', 'transcript': transcript, 'confidence': result.alternatives[0].confidence}
        else:
            print(f"Partial transcript: {transcript}")
            # Interim results can be used for live captioning display
            yield {'type': 'partial', 'transcript': transcript}
