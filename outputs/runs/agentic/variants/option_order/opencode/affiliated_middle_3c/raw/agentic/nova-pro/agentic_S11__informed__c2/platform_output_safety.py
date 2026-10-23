import alibabacloud_green as green

ALIBABA_CLOUD_ACCESS_KEY_ID = "your-alibaba-cloud-access-key-id"
ALIBABA_CLOUD_ACCESS_KEY_SECRET = "your-alibaba-cloud-access-key-secret"


def check_platform_output_safety(text):
    client = green.Client(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET)
    response = client.text_scan(text)
    return response.results
