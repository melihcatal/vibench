import alibabacloud_green


def vendor_text_safety(vendor_notes):
    client = alibabacloud_green.Client(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    safety_check = client.check_text(vendor_notes)
    return safety_check
