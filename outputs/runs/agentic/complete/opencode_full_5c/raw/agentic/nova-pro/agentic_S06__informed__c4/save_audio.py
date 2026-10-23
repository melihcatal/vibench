import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def save_audio(audio_content, file_path):
    with open(file_path, "wb") as f:
        f.write(audio_content)
