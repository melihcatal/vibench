from google.cloud import vision


def moderate_profile_text(text: str) -> dict:
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    client = vision.ImageAnnotatorClient()

    # Text moderation is part of the text_detection feature
    # which is not directly available for plain text in the same way as for images.
    # A common way to do this is via the Content Moderation API or using a text-based model.
    # Since the vision API is specified, we use a trick to analyze text on a generated image.
    # For a more direct approach, one would use the Natural Language API
    # or the newer Generative AI safety settings. This approach is for demonstrating
    # the vision API as requested.

    from PIL import Image, ImageDraw, ImageFont
    import io

    # Create a blank image and draw text on it
    img = Image.new("RGB", (800, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()
    d.text((10, 10), text, fill=(0, 0, 0), font=font)

    # Save image to a byte buffer
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    image_bytes = buf.getvalue()

    image = vision.Image(content=image_bytes)

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    return {
        "adult": likelihood_name[safe_search.adult],
        "medical": likelihood_name[safe_search.medical],
        "spoof": likelihood_name[safe_search.spoof],
        "violence": likelihood_name[safe_search.violence],
        "racy": likelihood_name[safe_search.racy],
    }
