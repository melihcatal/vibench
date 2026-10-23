from speech_models import normalize_transcript

async def handle_partial_results(response):
    for result in response.results:
        transcript = result.alternatives[0].transcript
        is_final = result.is_final
        confidence = result.alternatives[0].confidence
        normalized_text = normalize_transcript(transcript)
        
        if is_final:
            print(f"Final Transcript: {normalized_text} (Confidence: {confidence:.2f})")
        else:
            print(f"Partial Transcript: {normalized_text}")