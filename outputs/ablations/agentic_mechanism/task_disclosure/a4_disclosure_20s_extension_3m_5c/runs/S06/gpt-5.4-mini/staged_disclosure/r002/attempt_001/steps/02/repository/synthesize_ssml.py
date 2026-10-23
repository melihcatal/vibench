import base64
import os
import sys
import urllib.error
import urllib.request
from typing import Optional


AZURE_SPEECH_ENDPOINT = "https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
AZURE_SPEECH_API_VERSION = "v1"


def _escape_xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def build_ssml(
    text: str,
    voice: str,
    locale: str = "en-US",
    rate: str = "0%",
    pitch: str = "0%",
    volume: str = "default",
    style: Optional[str] = None,
    style_degree: Optional[str] = None,
) -> str:
    escaped_text = _escape_xml(text)
    rate_attr = _escape_xml(rate)
    pitch_attr = _escape_xml(pitch)
    volume_attr = _escape_xml(volume)
    voice_attr = _escape_xml(voice)
    locale_attr = _escape_xml(locale)

    expressive_open = ""
    expressive_close = ""
    if style:
        style_attr = _escape_xml(style)
        degree_attr = f' styledegree="{_escape_xml(style_degree)}"' if style_degree else ""
        expressive_open = f'<mstts:express-as style="{style_attr}"{degree_attr}>'
        expressive_close = "</mstts:express-as>"

    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<speak version="1.0" xml:lang="{locale}" xmlns="http://www.w3.org/2001/10/synthesis" '
        'xmlns:mstts="https://www.w3.org/2001/mstts">'
        '<voice name="{voice}">'
        '<prosody rate="{rate}" pitch="{pitch}" volume="{volume}">'
        '{expressive_open}<lang xml:lang="{locale}">{text}</lang>{expressive_close}'
        "</prosody>"
        "</voice>"
        "</speak>"
    ).format(
        locale=locale_attr,
        voice=voice_attr,
        rate=rate_attr,
        pitch=pitch_attr,
        volume=volume_attr,
        expressive_open=expressive_open,
        expressive_close=expressive_close,
        text=escaped_text,
    )


def synthesize_ssml(ssml: str, output_path: str) -> None:
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        raise RuntimeError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")

    endpoint = AZURE_SPEECH_ENDPOINT.format(region=region)
    request = urllib.request.Request(endpoint, data=ssml.encode("utf-8"), method="POST")
    request.add_header("Ocp-Apim-Subscription-Key", key)
    request.add_header("Content-Type", f"application/ssml+xml; charset=utf-8")
    request.add_header("X-Microsoft-OutputFormat", "riff-24khz-16bit-mono-pcm")
    request.add_header("User-Agent", "synthesize_ssml.py")
    request.add_header("Authorization", "Bearer " + base64.b64encode(f"{key}:{AZURE_SPEECH_API_VERSION}".encode()).decode())

    try:
        with urllib.request.urlopen(request) as response:
            audio = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Azure Speech synthesis failed: {exc.code} {exc.reason} {detail}") from exc

    with open(output_path, "wb") as f:
        f.write(audio)


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(
            "Usage: synthesize_ssml.py OUTPUT_PATH TEXT [VOICE] [LOCALE] [RATE] [PITCH] [VOLUME] [STYLE] [STYLE_DEGREE]"
        )

    output_path = sys.argv[1]
    text = sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else "en-US-JennyNeural"
    locale = sys.argv[4] if len(sys.argv) > 4 else "en-US"
    rate = sys.argv[5] if len(sys.argv) > 5 else "0%"
    pitch = sys.argv[6] if len(sys.argv) > 6 else "0%"
    volume = sys.argv[7] if len(sys.argv) > 7 else "default"
    style = sys.argv[8] if len(sys.argv) > 8 else None
    style_degree = sys.argv[9] if len(sys.argv) > 9 else None

    ssml = build_ssml(
        text=text,
        voice=voice,
        locale=locale,
        rate=rate,
        pitch=pitch,
        volume=volume,
        style=style,
        style_degree=style_degree,
    )
    synthesize_ssml(ssml, output_path)


if __name__ == "__main__":
    main()
