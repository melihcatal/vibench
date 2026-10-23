from google.cloud.texttospeech_v1.types import SynthesizeSpeechResponse

def save_audio_to_file(response: SynthesizeSpeechResponse, file_path: str):
    with open(file_path, "wb") as out_file:
        out_file.write(response.audio_content)

def save_audio_bytes(audio_content: bytes, file_path: str):
    with open(file_path, "wb") as out_file:
        out_file.write(audio_content)
