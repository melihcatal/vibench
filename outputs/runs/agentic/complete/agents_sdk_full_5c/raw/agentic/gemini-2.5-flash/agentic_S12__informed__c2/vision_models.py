from dataclasses import dataclass, field
import base64

@dataclass
class VisionImageInput:
    image_bytes: bytes = field(default_factory=bytes)
    image_uri: str = ""

    @classmethod
    def from_base64(cls, base64_string: str):
        return cls(image_bytes=base64.b64decode(base64_string))

    @classmethod
    def from_uri(cls, uri: str):
        return cls(image_uri=uri)

@dataclass
class ImageLabelsResult:
    labels: list[str]

@dataclass
class ImageDescriptionResult:
    description: str

@dataclass
class ImageTextResult:
    text: str

@dataclass
class ImageSafetyResult:
    adult: str
    medical: str
    violence: str
    racy: str
    spoof: str


if __name__ == '__main__':
    # Example usage
    input_bytes = VisionImageInput(image_bytes=b"some_image_bytes")
    print(f"Image input from bytes: {input_bytes}")

    input_uri = VisionImageInput.from_uri("gs://my-bucket/image.jpg")
    print(f"Image input from URI: {input_uri}")

    labels_res = ImageLabelsResult(labels=["cat", "animal"])
    print(f"Labels result: {labels_res}")
