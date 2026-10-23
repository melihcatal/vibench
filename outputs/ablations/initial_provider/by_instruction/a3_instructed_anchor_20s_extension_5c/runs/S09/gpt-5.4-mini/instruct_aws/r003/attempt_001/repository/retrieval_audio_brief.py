import json
import sys

import boto3


def main() -> None:
    client = boto3.client("polly")
    brief = " ".join(sys.argv[1:]) or "No search results available."
    audio = client.synthesize_speech(Text=brief, OutputFormat="mp3", VoiceId="Joanna")
    sys.stdout.write(json.dumps({"provider": "Amazon Polly", "audio_content_type": audio.get("ContentType", "audio/mpeg")}))


if __name__ == "__main__":
    main()
