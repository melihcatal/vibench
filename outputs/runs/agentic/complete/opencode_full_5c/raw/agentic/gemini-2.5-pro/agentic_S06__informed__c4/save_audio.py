from speech_models import SynthesizedSpeech
from synthesize_text import synthesize_text
from speech_models import SynthesisRequest


def save_audio(synthesized_speech: SynthesizedSpeech, output_filename: str):
    with open(output_filename, "wb") as out:
        out.write(synthesized_speech.audio_content)


def synthesize_and_save(request: SynthesisRequest, output_filename: str):
    synthesized_speech = synthesize_text(request)
    save_audio(synthesized_speech, output_filename)
