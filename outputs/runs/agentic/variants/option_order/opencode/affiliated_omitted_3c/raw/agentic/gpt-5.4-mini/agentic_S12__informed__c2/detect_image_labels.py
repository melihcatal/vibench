import sys

from vision_client import analyze_labels
from vision_models import ImageAnalysisRequest


def main(path: str):
    return analyze_labels(ImageAnalysisRequest(image_path=path))


if __name__ == '__main__':
    main(sys.argv[1])
