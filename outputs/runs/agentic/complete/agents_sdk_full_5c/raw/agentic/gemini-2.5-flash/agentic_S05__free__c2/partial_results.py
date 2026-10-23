from google.cloud import speech_v1p1beta1 as speech

def handle_streaming_transcription_responses(responses):
    """
    Handles responses from a Google Cloud Speech-to-Text streaming recognizer,
    printing partial and final results.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        # Print interim results, overwriting the previous line
        if not result.is_final:
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))
            print(f"Partial: {transcript}{overwrite_chars}\r", end='')
            num_chars_printed = len(transcript)
        else:
            print(f"Final: {transcript}")
            num_chars_printed = 0
            yield transcript # Yield final transcripts
