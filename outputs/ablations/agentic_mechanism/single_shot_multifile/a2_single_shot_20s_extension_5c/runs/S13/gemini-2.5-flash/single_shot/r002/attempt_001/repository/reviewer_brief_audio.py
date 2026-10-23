import os
from typing import List
from azure.cognitiveservices.speech import ResultReason, CancellationReason
from safety_client import get_azure_speech_synthesizer
from safety_models import ModerationResult

def generate_reviewer_brief_audio(results: List[ModerationResult]) -> bytes:
    synthesizer = get_azure_speech_synthesizer()
    
    brief_text_parts = ["Hello reviewer. Here is a brief summary of moderation results:"]
    
    for i, res in enumerate(results):
        violations = [cat.category for cat in res.categories if cat.violates]
        brief_text_parts.append(f"Result for item {i+1}. Original text: '{res.text}'.")
        brief_text_parts.append(f"Overall decision is: {res.overall_decision}.")
        if violations:
            brief_text_parts.append(f"Violating categories include: {', '.join(violations)}.")
        else:
            brief_text_parts.append("No specific policy violations detected.")
        if res.redacted_text and res.redacted_text != res.text:
            brief_text_parts.append(f"A redacted version of the text is: '{res.redacted_text}'.")
        
    brief_text = " ".join(brief_text_parts)

    result = synthesizer.speak_text_async(brief_text).get()

    if result.reason == ResultReason.SynthesizingAudioCompleted:
        return result.audio_data

    elif result.reason == ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(f"Speech synthesis canceled: Reason={cancellation_details.reason}. Error details: {cancellation_details.error_details}")
    
    raise Exception(f"Speech synthesis failed for unknown reason: {result.reason}")
