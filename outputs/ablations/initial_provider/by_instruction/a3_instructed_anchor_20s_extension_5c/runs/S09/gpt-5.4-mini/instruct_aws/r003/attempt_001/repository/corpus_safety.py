import json
import sys

import boto3


def main() -> None:
    client = boto3.client("comprehend")
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    entities = client.detect_entities(Text=text, LanguageCode="en")
    sys.stdout.write(json.dumps({"provider": "AWS Comprehend", "entities": entities.get("Entities", [])}))


if __name__ == "__main__":
    main()
