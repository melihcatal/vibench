import alibabacloud_green

ALIBABA_CLOUD_ACCESS_KEY_ID = "your_alibaba_cloud_access_key_id"
ALIBABA_CLOUD_ACCESS_KEY_SECRET = "your_alibaba_cloud_access_key_secret"

client = alibabacloud_green.Client(
    ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET
)


def live_caption_safety():
    # Check live transcript text for unsafe content
    pass
