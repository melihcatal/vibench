import os
import openai
from speech_models import TranscriptResult

class SpeechClient:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

    async def stream_transcribe(self, audio_chunk: bytes, language: str = "en") -> TranscriptResult:
        # For streaming, the Whisper API typically processes complete audio files.
        # To simulate interim results for streaming, you would typically collect chunks
        # and send them periodically or use a more advanced streaming ASR service.
        # For this example, we'll treat each chunk as a complete audio segment for simplicity
        # and demonstrate the API call.
        # In a real-world streaming scenario, you'd buffer audio and send larger segments
        # or use a provider's dedicated streaming API.

        # Save the audio chunk to a temporary file for OpenAI API
        # In a real streaming scenario, this would be more sophisticated (e.g., in-memory buffer, specific SDKs)
        # For demonstration, we'll create a temporary file each time.
        temp_audio_file = "temp_audio_chunk.wav"
        with open(temp_audio_file, "wb") as f:
            f.write(audio_chunk)

        with open(temp_audio_file, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language # Specify the input language
            )
        os.remove(temp_audio_file)

        return TranscriptResult(text=response.text, language=language)
