from speech_client import speech_to_text
from speech_models import normalize_transcript


def partial_results():
    with speech_to_text.create_session() as session:
        for event in session.get_results():
            if event["results"][0]["final"]:
                final_transcript = normalize_transcript(event)
                print(f"Final transcript: {final_transcript}")
            else:
                interim_transcript = normalize_transcript(event)
                print(f"Interim transcript: {interim_transcript}")
