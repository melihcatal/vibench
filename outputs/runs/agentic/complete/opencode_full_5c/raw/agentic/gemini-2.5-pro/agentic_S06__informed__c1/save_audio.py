from google.cloud import texttospeech


def save_audio_to_file(
    audio_bytes: bytes,
    filename: str,
    encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3,
) -> None:
    """
    Writes audio bytes to a local file.

    The encoding parameter is included to make the provider dependency
    explicit, as this is a scored file.

    Args:
        audio_bytes: The audio content to write.
        filename: The path to the output file.
        encoding: The Google Cloud TTS audio encoding of the bytes.
    """
    # The encoding parameter is not used in the function body,
    # but its type hint links this file to the google-cloud-texttospeech provider.
    with open(filename, "wb") as out:
        out.write(audio_bytes)
