from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple


@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float


@dataclass
class OcrWord:
    text: str
    confidence: float
    bounding_box: BoundingBox


@dataclass
class OcrLine:
    text: str
    words: List[OcrWord]
    confidence: float
    bounding_box: BoundingBox


@dataclass
class OcrBlock:
    block_type: str
    text: str
    confidence: float
    bounding_box: BoundingBox
    children: List["OcrBlock"] = field(default_factory=list)


@dataclass
class TableCell:
    text: str
    row_index: int
    col_index: int
    row_span: int
    col_span: int
    confidence: float
    bounding_box: BoundingBox


@dataclass
class TableRow:
    cells: List[TableCell]
    row_index: int


@dataclass
class Table:
    rows: List[TableRow]
    confidence: float
    bounding_box: BoundingBox


@dataclass
class KeyValue:
    key: str
    value: str
    confidence: float
    key_bounding_box: Optional[BoundingBox] = None
    value_bounding_box: Optional[BoundingBox] = None


@dataclass
class OcrTextResponse:
    full_text: str
    lines: List[OcrLine]
    words: List[OcrWord]
    page_width: int
    page_height: int
    confidence: float


@dataclass
class LayoutResponse:
    blocks: List[OcrBlock]
    lines: List[OcrLine]
    page_width: int
    page_height: int


@dataclass
class TableResponse:
    tables: List[Table]
    page_width: int
    page_height: int


@dataclass
class KeyValueResponse:
    key_values: List[KeyValue]
    page_width: int
    page_height: int


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class SafetyResponse:
    is_safe: bool
    scores: Dict[str, float]
    flagged_attributes: List[str]


@dataclass
class FieldExtractionResponse:
    fields: Dict[str, Any]
    confidence: float
    raw_text: str


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    section_texts: List[str]
    model: str


def normalize_bounding_box_polygon(
    polygon_points: List[Tuple[float, float]],
) -> BoundingBox:
    xs = [p[0] for p in polygon_points]
    ys = [p[1] for p in polygon_points]
    return BoundingBox(
        x=min(xs),
        y=min(ys),
        width=max(xs) - min(xs),
        height=max(ys) - min(ys),
    )


def normalize_confidence(value: Optional[float]) -> float:
    if value is None:
        return 0.0
    return max(0.0, min(1.0, value))


def join_words_to_lines(words: List[OcrWord]) -> List[OcrLine]:
    lines: List[OcrLine] = []
    current_words: List[OcrWord] = []
    current_y: Optional[float] = None

    for word in words:
        word_center_y = word.bounding_box.y + word.bounding_box.height / 2
        if (
            current_y is None
            or abs(word_center_y - current_y) > word.bounding_box.height * 0.5
        ):
            if current_words:
                line_text = " ".join(w.text for w in current_words)
                line_bbox = normalize_bounding_box_polygon(
                    [(w.bounding_box.x, w.bounding_box.y) for w in current_words]
                    + [
                        (
                            w.bounding_box.x + w.bounding_box.width,
                            w.bounding_box.y + w.bounding_box.height,
                        )
                        for w in current_words
                    ]
                )
                avg_conf = sum(w.confidence for w in current_words) / len(current_words)
                lines.append(
                    OcrLine(
                        text=line_text,
                        words=current_words,
                        confidence=normalize_confidence(avg_conf),
                        bounding_box=line_bbox,
                    )
                )
            current_words = [word]
            current_y = word_center_y
        else:
            current_words.append(word)

    if current_words:
        line_text = " ".join(w.text for w in current_words)
        line_bbox = normalize_bounding_box_polygon(
            [(w.bounding_box.x, w.bounding_box.y) for w in current_words]
            + [
                (
                    w.bounding_box.x + w.bounding_box.width,
                    w.bounding_box.y + w.bounding_box.height,
                )
                for w in current_words
            ]
        )
        avg_conf = sum(w.confidence for w in current_words) / len(current_words)
        lines.append(
            OcrLine(
                text=line_text,
                words=current_words,
                confidence=normalize_confidence(avg_conf),
                bounding_box=line_bbox,
            )
        )

    return lines


def build_full_text(lines: List[OcrLine]) -> str:
    return "\n".join(line.text for line in lines)
