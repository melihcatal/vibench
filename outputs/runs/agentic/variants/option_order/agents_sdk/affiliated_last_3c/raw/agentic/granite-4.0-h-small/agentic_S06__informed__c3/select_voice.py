from speech_client import TextToSpeechClient  # Azure provider

def list_voices():
    client = TextToSpeechClient()
    voices = client.list_voices()
    for v in voices:
        print(f"{v.name} | {v.language_code} | {v.gender} | {v.style}")

# Example: select a voice matching locale 'en-US'
if __name__ == '__main__':
    list_voices()
