import sys

from vision_client import client, load_image_bytes
from vision_models import ImageAnalysisRequest


def main(path: str):
    req = ImageAnalysisRequest(image_path=path)
    response = client().detect_labels(Image={'Bytes': load_image_bytes(req.image_path)}, MaxLabels=5)
    labels = response.get('Labels', [])
    return ', '.join(item.get('Name', '') for item in labels[:3])


if __name__ == '__main__':
    main(sys.argv[1])
