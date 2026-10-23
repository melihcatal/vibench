import dashscope

# Fetch available voices from the TTS service (CosyVoice demo)
def list_voices(locale: str = "en-US"):
    # In demo mode we return a static list; a real client would call the provider's list endpoint
    # Example endpoint: client.list_voices(locale=locale)  # placeholder
    return [
        {"name": "en-US-AlloyV2", "description": "A natural English US voice"},
        {"name": "en-GB-LiamV2", "description": "British English voice"},
        {"name": "zh-CN-XiaoyanV2", "description": "Mandarin Chinese voice"}
    ]

# Helper to pick a voice by name or interactive selection
def select_voice(locale: str = "en-US"):
    voices = list_voices(locale)
    if not voices:
        raise ValueError(f"No voices found for locale {locale}")
    print("Available voices:")
    for i, v in enumerate(voices, 1):
        print(f"{i}. {v['name']} - {v['description']}")
    choice = input("Enter the number of the desired voice: ")
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(voices):
            raise ValueError("Invalid selection")
        return voices[idx]["name"]
    except ValueError:
        print("Invalid input; using the first voice by default.")
        return voices[0]["name"]

# Example usage (remove if integrating as a library)
if __name__ == "__main__":
    voice_id = select_voice()
    print(f"Selected voice ID: {voice_id}")
