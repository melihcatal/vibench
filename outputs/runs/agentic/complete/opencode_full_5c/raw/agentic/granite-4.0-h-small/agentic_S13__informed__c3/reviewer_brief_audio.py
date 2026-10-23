# reviewer_brief_audio.py
# [LATER-STEP] Generate spoken briefs for moderation reviewers

# Provider selection – use Azure Speech TTS as an example
PROVIDER = "azure"


# -----------------------------------------------------------------------------
# Public API: create an audio brief summarizing a moderation decision
# -----------------------------------------------------------------------------
def generate_audio_brief(decision: dict, reviewer_name: str = "Reviewer") -> bytes:
    """Synthesize an audio brief from a moderation decision.

    Args:
        decision: Dictionary containing moderation details (e.g., unsafe, categories).
        reviewer_name: Name of the human reviewer for personalization.

    Returns:
        bytes: PCM audio data (WAV format) ready for playback.
    """
    import azure.cognitiveservices.speech as speechsdk
    from io import BytesIO

    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )

    # Build a concise spoken script based on the decision
    unsafe = decision.get("unsafe", False)
    categories = decision.get("categories", [])
    script = f"Hello {reviewer_name}. This message has been flagged."
    if unsafe:
        if categories:
            scripts = [
                f"Category {cat}: {details.get('severity', 'moderate')}"
                for cat, details in categories.items()
            ]
            script += " \nDetected issues: " + ", ".join(scripts)
        else:
            script += " No specific categories were identified."
    script += " Please review the case."

    # Perform text-to-speech synthesis
    audio_config = speechsdk.audio.AudioOutputConfig(
        filename=None
    )  # Output to in‑memory stream
    synth = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = synth.speak_text_async(script).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_bytes = BytesIO(result.audio_data)
        return audio_bytes.getvalue()
    else:
        raise RuntimeError(f"Speech synthesis failed with reason: {result.reason}")


# Example (would be in a driver script):
# decision = {"unsafe": True, "categories": {"harassment": {"severity": "moderate"}}}
# wav = generate_audio_brief(decision, reviewer_name="Alice")
# with open("brief.wav", "wb") as f: f.write(wav)
