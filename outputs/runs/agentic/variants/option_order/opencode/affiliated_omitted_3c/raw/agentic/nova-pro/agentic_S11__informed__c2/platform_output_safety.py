import alibabacloud_green as green


def check_platform_output_for_unsafe_content(text):
    client = green.Client(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    request = green.DetectTextRequest(text=text)
    response = client.detect_text(request)
    return response.result
