from synthesize_text import synthesize_text
from speech_models import SpeechSynthesisRequest


def save_audio(request: SpeechSynthesisRequest, output_path: str):
    response = synthesize_text(request)
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
