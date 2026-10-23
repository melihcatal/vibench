import os
import dashscope

# DashScope API key for TTS
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

def generate_spoken_brief(text: str, voice: str = "zh-Yue-Max") -> bytes:
    """Generates spoken (audio) output from model text using DashScope CosyVoice.

    Returns raw byte stream (WAV) that can be saved or streamed.
    """
    response = dashscope.tts.create(
        model="cosyvoice",
        voice=voice,
        text=text,
        audio_format="wav"
    )
    # response.raw.audio_bytes contains the binary WAV data
    return response.raw.audio_bytes

# Example CLI helper (optional)
# if __name__ == "__main__":
#     audio = generate_spoken_brief("Hello, this is a brief summary of today's meeting.")
#     with open("brief.wav", "wb") as f:
#         f.write(audio)
