import alibabacloud_green20231227 as green
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_green20231227.models import TextScanRequest


def check_safety(text: str):
    config = green.Config(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    client = green.Client(config)
    request = TextScanRequest(data=text)
    response = client.text_scan(request)
    return response.body.results[0].scenes
