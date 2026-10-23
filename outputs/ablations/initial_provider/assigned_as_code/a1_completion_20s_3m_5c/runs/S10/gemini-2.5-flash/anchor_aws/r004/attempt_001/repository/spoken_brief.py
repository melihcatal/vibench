from model_client import BedrockModelClient
from model_models import SynthesizeSpeechRequest
import io

def generate_spoken_brief(payload: SynthesizeSpeechRequest, config=None):
    client = BedrockModelClient(region_name=config.get("region") if config else None)

    audio_stream = client.synthesize_speech(request=payload)
    
    # The audio_stream is a botocore.response.StreamingBody object.
    # For practical use, you might want to save it to a file or stream it directly.
    # Here we simulate returning the raw audio bytes.
    audio_bytes = audio_stream.read()

    # You could also save it to a temporary file:
    # with open("spoken_brief.mp3", "wb") as f:
    #     f.write(audio_bytes)
    
    return {"audio_content": audio_bytes, "output_format": payload.output_format}
