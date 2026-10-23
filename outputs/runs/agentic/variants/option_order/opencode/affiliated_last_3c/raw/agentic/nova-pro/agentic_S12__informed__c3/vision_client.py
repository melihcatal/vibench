import google.cloud.vision as vision


def create_vision_client():
    return vision.ImageAnnotatorClient()
