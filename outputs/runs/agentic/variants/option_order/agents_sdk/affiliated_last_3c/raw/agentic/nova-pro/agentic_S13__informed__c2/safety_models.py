from alibabacloud_green20180509 import models as green_models

def create_image_scan_request(text):
    request = green_models.ImageScanRequest()
    request.image_url = text
    return request