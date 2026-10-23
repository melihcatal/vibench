# reviewer_brief_audio.py
import json
from safety_models import ModerationResponse
from google.cloud import texttospeech

def generate_audio_brief(responses: List[ModerationResponse], output_path: str = "brief.mp3") -> None:
    """Create a spoken brief for moderation reviewers summarizing decisions.

    Uses Google Cloud Text-to-Speech as the concrete provider.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text="Moderation Summary:\\n")
    # Simple concatenation of each decision.
    for resp in responses:
        synthesis_input.text += f"Text \"{resp.text[:30]}...\" – {resp.decision}\\n"
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio brief written to {output_path}")

if __name__ == "__main__":
    # Demo with synthetic ModerationResponse objects.
    from safety_models import ModerationResponse
    demo = [
        ModerationResponse(text="You are an idiot.", decision="REJECT"),
        ModerationResponse(text="Nice post!", decision="ALLOW")
    ]
    generate_audio_brief(demo)
