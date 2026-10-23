import alibabacloud_green

config = alibabacloud_green.Config(
    access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)
client = alibabacloud_green.Client(config)


def visual_safety_text(text):
    response = client.text_scan(text)
    return response["results"][0]["label"]
