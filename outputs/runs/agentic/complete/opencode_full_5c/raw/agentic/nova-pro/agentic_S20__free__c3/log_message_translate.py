import boto3
import translate

cw_logs = boto3.client("logs", region_name="us-west-2")
translate_client = translate.Client()

log_group_name = "MyLogGroup"


def translate_log_message(log_message, target_language):
    translation = translate_client.translate_text(log_message, target_language)
    return translation


if __name__ == "__main__":
    log_message = "This is a sample log message."
    target_language = "es"
    translated_message = translate_log_message(log_message, target_language)
    print(translated_message)
