import os
from dashscope import Audio


def platform_brief_audio(text: str, output_path: str = "output.wav"):
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set.")

    result = Audio.SpeechSynthesizer.call(
        model="cosyvoice-v1", text=text, format="wav", api_key=api_key
    )

    if result.get_audio_data() is not None:
        with open(output_path, "wb") as f:
            f.write(result.get_audio_data())
        return {"status": "success", "output_file": output_path}
    else:
        raise Exception(f"Audio generation failed: {result.get_response().message}")
