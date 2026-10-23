def save_audio(audio_content: bytes, filename: str):
    with open(filename, "wb") as out:
        out.write(audio_content)
    print(f'Audio content written to file "{filename}" ')
