def save_audio_content(audio_content, filename):
    with open(filename, "wb") as out:
        out.write(audio_content)
    return f"Audio content written to {filename}"
