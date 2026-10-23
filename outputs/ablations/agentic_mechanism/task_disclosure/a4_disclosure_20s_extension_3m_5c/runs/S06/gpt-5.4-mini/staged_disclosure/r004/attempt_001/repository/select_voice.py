import os
import sys
import urllib.error
import urllib.parse
import urllib.request


OPENAI_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def select_voice(target_locale: str, available_voices=None) -> str:
    available_voices = available_voices or OPENAI_VOICES
    locale = (target_locale or "").strip().lower()
    if locale.startswith(("en", "en-")):
        preferred = ["alloy", "nova", "echo"]
    elif locale.startswith(("es", "es-")):
        preferred = ["nova", "alloy", "shimmer"]
    elif locale.startswith(("fr", "fr-")):
        preferred = ["shimmer", "nova", "alloy"]
    elif locale.startswith(("de", "de-")):
        preferred = ["onyx", "alloy", "echo"]
    elif locale.startswith(("ja", "ja-")):
        preferred = ["shimmer", "nova", "echo"]
    else:
        preferred = ["alloy", "nova", "echo"]
    for voice in preferred:
        if voice in available_voices:
            return voice
    return available_voices[0] if available_voices else "alloy"


def list_openai_tts_voices() -> list[str]:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return OPENAI_VOICES[:]
    request = urllib.request.Request(
        "https://api.openai.com/v1/audio/speech",
        data=urllib.parse.urlencode({"model": "gpt-4o-mini-tts", "input": "test", "voice": "alloy"}).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10):
            pass
    except urllib.error.HTTPError:
        pass
    except urllib.error.URLError:
        pass
    return OPENAI_VOICES[:]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python select_voice.py <locale> [--list]")
        return 2
    locale = sys.argv[1]
    voices = list_openai_tts_voices()
    if len(sys.argv) > 2 and sys.argv[2] == "--list":
        print("\n".join(voices))
        return 0
    print(select_voice(locale, voices))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
