import os
from safety_models import SafetyModels

def reviewer_brief_audio(reasons: list[str]) -> str:
    """Generate a concise spoken brief for moderation reviewers.
    Returns a string that can be fed into a TTS service.
    """
    # Concatenate reasons into a short human-readable script
    script = 'Moderation review brief:\n'
    for i, reason in enumerate(reasons, start=1):
        script += f'{i}. {reason}\n'
    return script

# Example of calling a Text-to-Speech service (commented out)
# from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer
# def synthesize_audio(text):
#     speech_config = SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'), region=os.getenv('AZURE_SPEECH_REGION'))
#     audio_config = AudioConfig(output_format=AudioOutputFormat.WAVE_FORMAT_16BITPCM)
#     synth = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
#     result = synth.speak_text_async(text).get()
#     return result.get_audio_data()
# audio_bytes = synthesize_audio(reviewer_brief_audio(['Hate speech', 'Violence']))
# with open('moderation_brief.wav', 'wb') as f: f.write(audio_bytes)
