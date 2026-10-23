import sys

from vision_client import analyze_safety
from vision_models import ImageAnalysisRequest


def main(path: str):
    return analyze_safety(ImageAnalysisRequest(image_path=path))


if __name__ == '__main__':
    main(sys.argv[1])
