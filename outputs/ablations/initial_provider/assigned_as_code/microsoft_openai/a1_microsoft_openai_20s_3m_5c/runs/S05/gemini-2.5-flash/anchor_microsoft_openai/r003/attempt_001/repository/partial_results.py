from typing import Generator, Dict, Any
from speech_models import SpeechRecognitionResult

def partial_results_handler(event_stream: Generator[SpeechRecognitionResult, None, None]):
    for result in event_stream:
        if result.is_final:
            print(f"Final: {result.text}")
        else:
            print(f"Partial: {result.text}")

def collect_partial_results(event_stream: Generator[SpeechRecognitionResult, None, None]) -> Dict[str, Any]:
    final_transcript_parts = []
    partial_transcript = ""
    for result in event_stream:
        if result.is_final:
            if partial_transcript:
                # If there was a partial before a final, store it as a completed part
                final_transcript_parts.append(partial_transcript.strip())
            final_transcript_parts.append(result.text.strip())
            partial_transcript = ""  # Reset partial after a final result
        else:
            partial_transcript = result.text

    # Add any remaining partial as a final part if the stream ends without a final event
    if partial_transcript:
        final_transcript_parts.append(partial_transcript.strip())
        
    return {"full_transcript": " ".join(final_transcript_parts).strip()}
