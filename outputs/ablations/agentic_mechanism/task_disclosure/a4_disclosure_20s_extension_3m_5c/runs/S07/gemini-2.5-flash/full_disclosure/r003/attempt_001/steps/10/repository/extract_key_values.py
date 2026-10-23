from google.cloud import vision_v1p4beta1 as vision
import os

def extract_key_values_from_document(image_content: bytes):
    """
    Extracts key-value pairs from a form-like document using Google Cloud Vision API.

    Args:
        image_content: The content of the document image in bytes.

    Returns:
        A dictionary of extracted key-value pairs.
    """
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=image_content)

    # Set up feature to detect document text (which includes form parsing)
    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION,
        model="builtin/stable",  # Use stable model for document text detection
    )
    request = vision.AnnotateImageRequest(image=image, features=[feature])
    response = client.annotate_image(request=request)

    document = response.full_text_annotation
    
    key_value_pairs = {}
    if document and document.pages:
        for page in document.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    # This is a simplified approach. For more robust key-value extraction,
                    # especially from complex forms, one would typically need to implement
                    # more advanced logic to associate text segments as keys and values,
                    # possibly involving spatial analysis or machine learning models
                    # trained for form parsing.
                    # Google Cloud Vision API's DOCUMENT_TEXT_DETECTION provides
                    # hierarchical structure, but direct key-value pairing from it
                    # might require additional post-processing.
                    # For demonstration purposes, we'll just extract text here.
                    for word in paragraph.words:
                        word_text = "".join([symbol.text for symbol in word.symbols])
                        # In a real-world scenario, you would analyze the layout
                        # and text relationships to identify actual key-value pairs.
                        # This example just shows that text can be extracted.
                        pass # Placeholder for actual key-value logic

    # The Vision API's DOCUMENT_TEXT_DETECTION feature does not directly return
    # "key-value pairs" as a distinct object. It provides a hierarchical structure
    # of text (pages, blocks, paragraphs, words) along with their bounding boxes.
    # To extract key-value pairs, custom post-processing logic is typically
    # required to analyze the spatial relationship and content of the extracted text.
    # For a more advanced solution for structured data extraction from forms,
    # Google Cloud Document AI would be a more specialized service.

    # This example returns a placeholder indicating that custom logic is needed.
    # In a real implementation, you would populate `key_value_pairs`
    # by processing `document.pages`.

    # Example of how to iterate through entities if using Document AI,
    # which is more suited for key-value extraction.
    # If using Document AI, you would replace the above with a Document AI client.
    # from google.cloud import documentai_v1 as documentai
    # client = documentai.DocumentProcessorServiceClient()
    # document = client.process_document(...)
    # for entity in document.entities:
    #    if entity.type == "KEY_VALUE_PAIR":
    #        key_text = entity.mention_text
    #        value_text = ""
    #        for prop in entity.properties:
    #            if prop.type == "VALUE":
    #                value_text = prop.mention_text
    #                break
    #        key_value_pairs[key_text] = value_text

    return {"status": "Key-value extraction requires custom post-processing logic from the Vision API's full_text_annotation or using Google Cloud Document AI."}

if __name__ == "__main__":
    # Example usage (replace with actual image content)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # with the path to your service account key file.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

    # Create a dummy image for demonstration
    from PIL import Image, ImageDraw, ImageFont
    import io

    def create_dummy_form_image(text="Name: John Doe\nDate: 2026-09-20"):
        img = Image.new('RGB', (400, 200), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        try:
            # Try to use a common font, or a default if not found
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
        d.text((10,10), text, fill=(0,0,0), font=font)
        
        byte_arr = io.BytesIO()
        img.save(byte_arr, format='PNG')
        return byte_arr.getvalue()

    dummy_image_content = create_dummy_form_image()
    
    print("Attempting to extract key-value pairs from a dummy document...")
    extracted_data = extract_key_values_from_document(dummy_image_content)
    print("Extracted Data:", extracted_data)

    # For a more realistic example, you would read an actual image file:
    # with open("path/to/your/form_document.png", "rb") as image_file:
    #     content = image_file.read()
    #     extracted_data = extract_key_values_from_document(content)
    #     print("Extracted Data:", extracted_data)
