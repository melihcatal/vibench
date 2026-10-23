import os
import http.client
import json

# Watson TTS credentials loaded from environment
WATSON_TTS_URL = os.getenv("IBM_TTS_URL")
WATSON_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")

VOICE_LANG_LOCALE = {
    # Map locale to Watson voice name example
    "en-US": "en-US_MichaelV3Voice",
    "en-GB": "en-GB_KateV3Voice",
    "es-ES": "es-ES_LauraV3Voice",
    "fr-FR": "fr-FR_ReneeV3Voice",
    # Add more as needed
}


def get_available_voices(locale: str) -> dict:
    """
    Calls Watson TTS /v1/voices endpoint to list voices for a locale.
    Returns the full JSON payload from the service.
    """
    if locale not in VOICE_LANG_LOCALE:
        raise ValueError(
            f"No predefined voice for locale {locale}. Add mapping or use custom voice name."
        )
    voice_name = VOICE_LANG_LOCALE[locale]
    connection = http.client.HTTPSConnection(WATSON_TTS_URL, timeout=10)
    connection.request(
        method="GET",
        url="/v1/voices",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"apikey {WATSON_TTS_APIKEY}",
        },
    )
    response = connection.getresponse()
    data = json.loads(response.read().decode())
    connection.close()
    return data


def select_voice(locale: str, voice_name: str = None) -> str:
    """
    Returns a voice name appropriate for the given locale. If voice_name is
    provided and exists for the locale, returns it; otherwise returns the
    default voice for that locale.
    """
    voices = get_available_voices(locale)
    voice_list = {v["name"]: v for v in voices["voices"]}
    if voice_name and voice_name in voice_list:
        return voice_name
    return voice_list[next(iter(voice_list))]  # default first entry


# Example raw call (kept commented)
# voices = get_available_voices('en-US')
# print(json.dumps(voices, indent=2))
