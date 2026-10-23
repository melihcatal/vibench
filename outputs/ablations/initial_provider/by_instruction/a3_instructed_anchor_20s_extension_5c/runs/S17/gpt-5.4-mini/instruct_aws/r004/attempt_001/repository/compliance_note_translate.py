import boto3

from security_client import load_security_client_config


def compliance_note_translate(text: str, target_language: str) -> dict:
    translate = boto3.client("translate", region_name=load_security_client_config().region_name)
    return translate.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language)


def main() -> None:
    compliance_note_translate("sample compliance note", "es")


if __name__ == "__main__":
    main()
