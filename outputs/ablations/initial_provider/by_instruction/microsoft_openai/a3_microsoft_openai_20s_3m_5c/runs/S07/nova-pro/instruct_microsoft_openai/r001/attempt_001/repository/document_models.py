from typing import List, Tuple

class DocumentModels:
    @staticmethod
    def normalize_text(text: str) -> str:
        return text.strip()

    @staticmethod
    def normalize_layout(layout: List[str]) -> List[str]:
        return [element.strip() for element in layout]

    @staticmethod
    def normalize_tables(tables: List[List[str]]) -> List[List[str]]:
        return [[cell.strip() for cell in row] for row in tables]

    @staticmethod
    def normalize_key_values(key_values: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        return [(key.strip(), value.strip()) for key, value in key_values]