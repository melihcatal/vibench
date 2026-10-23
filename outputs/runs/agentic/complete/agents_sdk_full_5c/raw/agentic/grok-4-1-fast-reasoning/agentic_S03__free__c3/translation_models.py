from typing import List, Union

def normalize_input(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """Normalize input text for translation."""
    if isinstance(text, str):
        return text.strip()
    return [t.strip() for t in text]

def denormalize_output(result_text: Union[str, List[str]]) -> Union[str, List[str]]:
    """Denormalize output text from translation."""
    return result_text  # DeepL preserves formatting