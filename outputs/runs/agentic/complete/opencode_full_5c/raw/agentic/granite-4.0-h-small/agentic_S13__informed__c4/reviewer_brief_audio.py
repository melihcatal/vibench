import os
from safety_models import SafetyModels
from azure.ai.speech import SpeechConfig, SpeechSynthesizer


def generate_spoken_brief(
    decision: str,
    rationale: str = "",
    brief_template: str = "Decision: {decision}. Reason: {rationale}.",
):
    """Generate a spoken brief for moderation reviewers using Azure Polly TTS.",
    Saves an MP3 file with the spoken audio.",
    """
    config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    synthesizer = SpeechSynthesizer(speech_config=config)
    speech = brief_template.format(decision=decision, rationale=rationale)
    audio_config = AudioConfig(filename="moderation_brief.mp3")
    result = synthesizer.speak_text_async(speech, audio_config=audio_config).get()
    print(f"Spoken brief generated: moderation_brief.mp3 (decision: {decision})")


if __name__ == "__main__":
    generate_spoken_brief(
        decision="unsafe", rationale="Contains high toxicity content."
    )
