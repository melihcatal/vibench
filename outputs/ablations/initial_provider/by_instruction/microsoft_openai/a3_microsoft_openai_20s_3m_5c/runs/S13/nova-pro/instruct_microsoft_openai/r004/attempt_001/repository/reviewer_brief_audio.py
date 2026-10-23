import pyttsx3

def reviewer_brief_audio(text: str, output_file: str):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_file)
    engine.runAndWait()