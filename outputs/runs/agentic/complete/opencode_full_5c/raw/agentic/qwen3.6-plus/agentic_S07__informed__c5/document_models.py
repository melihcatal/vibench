from dataclasses import dataclass, field
from typing import Any


@dataclass
class OcrTextResult:
    full_text: str = ""
    pages: list[dict[str, Any]] = field(default_factory=list)
    language: str = ""
    model_id: str = ""
    confidence: float = 0.0


@dataclass
class LayoutBlock:
    block_type: str = ""
    text: str = ""
    bounding_box: list[float] = field(default_factory=list)
    confidence: float = 0.0
    page_number: int = 0


@dataclass
class LayoutResult:
    paragraphs: list[LayoutBlock] = field(default_factory=list)
    sections: list[LayoutBlock] = field(default_factory=list)
    tables: list["TableResult"] = field(default_factory=list)
    figures: list[LayoutBlock] = field(default_factory=list)
    page_width: float = 0.0
    page_height: float = 0.0
    model_id: str = ""


@dataclass
class TableCell:
    row_index: int = 0
    column_index: int = 0
    text: str = ""
    is_header: bool = False
    confidence: float = 0.0
    bounding_box: list[float] = field(default_factory=list)


@dataclass
class TableResult:
    row_count: int = 0
    column_count: int = 0
    cells: list[TableCell] = field(default_factory=list)
    bounding_box: list[float] = field(default_factory=list)
    confidence: float = 0.0
    page_number: int = 0


@dataclass
class KeyValuePair:
    key: str = ""
    value: str = ""
    key_confidence: float = 0.0
    value_confidence: float = 0.0
    bounding_box: list[float] = field(default_factory=list)


@dataclass
class KeyValueResult:
    pairs: list[KeyValuePair] = field(default_factory=list)
    model_id: str = ""


@dataclass
class TranslationResult:
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    confidence: float = 0.0


@dataclass
class SafetyResult:
    is_safe: bool = True
    categories: dict[str, float] = field(default_factory=dict)
    severity: str = "safe"
    review_recommended: bool = False


@dataclass
class FieldValue:
    field_name: str = ""
    value: str = ""
    confidence: float = 0.0
    value_type: str = ""


@dataclass
class FieldExtractionResult:
    fields: list[FieldValue] = field(default_factory=list)
    model_id: str = ""
    document_type: str = ""


@dataclass
class EmbeddingResult:
    embeddings: list[list[float]] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)
    model: str = ""


def normalize_ocr_text(analyze_result) -> OcrTextResult:
    full_text = getattr(analyze_result, "content", "") or ""
    language = ""
    pages = []
    if hasattr(analyze_result, "pages") and analyze_result.pages:
        for page in analyze_result.pages:
            page_info = {"page_number": page.page_number, "lines": []}
            if hasattr(page, "lines") and page.lines:
                for line in page.lines:
                    page_info["lines"].append(line.content)
                    if not language and hasattr(line, "language"):
                        language = line.language or ""
            pages.append(page_info)
    return OcrTextResult(
        full_text=full_text,
        pages=pages,
        language=language,
        model_id=getattr(analyze_result, "model_id", ""),
    )


def normalize_layout_result(analyze_result) -> LayoutResult:
    paragraphs = []
    sections = []
    figures = []
    page_width = 0.0
    page_height = 0.0

    if hasattr(analyze_result, "paragraphs") and analyze_result.paragraphs:
        for para in analyze_result.paragraphs:
            role = getattr(para, "role", "") or ""
            block = LayoutBlock(
                block_type=role if role else "paragraph",
                text=para.content,
                bounding_box=_extract_bounding_box(para),
                confidence=1.0,
                page_number=_get_page_number(para),
            )
            if role in ("sectionHeading", "title"):
                sections.append(block)
            else:
                paragraphs.append(block)

    if hasattr(analyze_result, "figures") and analyze_result.figures:
        for fig in analyze_result.figures:
            figures.append(
                LayoutBlock(
                    block_type="figure",
                    text=getattr(fig, "caption", {}).get("content", "")
                    if hasattr(fig, "caption") and fig.caption
                    else "",
                    bounding_box=_extract_bounding_box(fig),
                    page_number=_get_page_number(fig),
                )
            )

    tables = []
    if hasattr(analyze_result, "tables") and analyze_result.tables:
        for tbl in analyze_result.tables:
            table_result = normalize_table_result(tbl)
            tables.append(table_result)

    if hasattr(analyze_result, "pages") and analyze_result.pages:
        first_page = analyze_result.pages[0]
        page_width = getattr(first_page, "width", 0.0) or 0.0
        page_height = getattr(first_page, "height", 0.0) or 0.0

    return LayoutResult(
        paragraphs=paragraphs,
        sections=sections,
        tables=tables,
        figures=figures,
        page_width=page_width,
        page_height=page_height,
        model_id=getattr(analyze_result, "model_id", ""),
    )


def normalize_table_result(table_obj) -> TableResult:
    cells = []
    if hasattr(table_obj, "cells") and table_obj.cells:
        for cell in table_obj.cells:
            cells.append(
                TableCell(
                    row_index=getattr(cell, "row_index", 0) or 0,
                    column_index=getattr(cell, "column_index", 0) or 0,
                    text=getattr(cell, "content", "") or "",
                    is_header=bool(getattr(cell, "is_header", False)),
                    confidence=getattr(cell, "confidence", 0.0) or 0.0,
                    bounding_box=_extract_bounding_box(cell),
                )
            )
    return TableResult(
        row_count=getattr(table_obj, "row_count", 0) or 0,
        column_count=getattr(table_obj, "column_count", 0) or 0,
        cells=cells,
        bounding_box=_extract_bounding_box(table_obj),
        confidence=getattr(table_obj, "confidence", 0.0) or 0.0,
        page_number=_get_page_number(table_obj),
    )


def normalize_key_value_result(analyze_result) -> KeyValueResult:
    pairs = []
    if hasattr(analyze_result, "key_value_pairs") and analyze_result.key_value_pairs:
        for kv in analyze_result.key_value_pairs:
            key_text = ""
            val_text = ""
            key_conf = 0.0
            val_conf = 0.0
            bb = []

            if hasattr(kv, "key") and kv.key:
                key_text = getattr(kv.key, "content", "") or ""
                key_conf = getattr(kv.key, "confidence", 0.0) or 0.0

            if hasattr(kv, "value") and kv.value:
                val_text = getattr(kv.value, "content", "") or ""
                val_conf = getattr(kv.value, "confidence", 0.0) or 0.0
                bb = _extract_bounding_box(kv.value)

            pairs.append(
                KeyValuePair(
                    key=key_text,
                    value=val_text,
                    key_confidence=key_conf,
                    value_confidence=val_conf,
                    bounding_box=bb,
                )
            )

    return KeyValueResult(
        pairs=pairs,
        model_id=getattr(analyze_result, "model_id", ""),
    )


def normalize_field_extraction_result(analyze_result) -> FieldExtractionResult:
    fields = []
    document_type = ""
    if hasattr(analyze_result, "documents") and analyze_result.documents:
        doc = analyze_result.documents[0]
        document_type = getattr(doc, "doc_type", "") or ""
        if hasattr(doc, "fields") and doc.fields:
            for field_name, field_obj in doc.fields.items():
                val = getattr(field_obj, "value", "") or ""
                if isinstance(val, dict):
                    val = str(val)
                fields.append(
                    FieldValue(
                        field_name=field_name,
                        value=str(val),
                        confidence=getattr(field_obj, "confidence", 0.0) or 0.0,
                        value_type=getattr(field_obj, "type", "") or "",
                    )
                )
    return FieldExtractionResult(
        fields=fields,
        model_id=getattr(analyze_result, "model_id", ""),
        document_type=document_type,
    )


def _extract_bounding_box(obj) -> list[float]:
    if hasattr(obj, "bounding_regions") and obj.bounding_regions:
        region = obj.bounding_regions[0]
        if hasattr(region, "polygon"):
            return list(region.polygon)
    if hasattr(obj, "bounding_box") and obj.bounding_box:
        bb = obj.bounding_box
        if hasattr(bb, "polygon"):
            return list(bb.polygon)
    return []


def _get_page_number(obj) -> int:
    if hasattr(obj, "bounding_regions") and obj.bounding_regions:
        return obj.bounding_regions[0].page_number
    return 0
