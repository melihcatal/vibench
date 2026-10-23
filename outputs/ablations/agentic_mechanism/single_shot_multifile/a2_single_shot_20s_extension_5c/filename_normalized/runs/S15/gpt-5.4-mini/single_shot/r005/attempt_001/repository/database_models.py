from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_document(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): normalize_document(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_document(v) for v in value]
    return value


@dataclass
class DocumentUpsertRequest:
    primary_key_name: str
    primary_key_value: str
    document: Dict[str, Any]
    version: Optional[int] = None
    version_field: str = "version"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentUpsertRequest":
        return cls(
            primary_key_name=data.get("primary_key_name", "id"),
            primary_key_value=str(data["primary_key_value"]),
            document=dict(data.get("document", {})),
            version=data.get("version"),
            version_field=data.get("version_field", "version"),
        )


@dataclass
class DocumentFetchRequest:
    primary_key_name: str
    primary_key_value: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentFetchRequest":
        return cls(primary_key_name=data.get("primary_key_name", "id"), primary_key_value=str(data["primary_key_value"]))


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    index_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentQueryRequest":
        return cls(field_name=data["field_name"], field_value=data["field_value"], index_name=data.get("index_name"))


@dataclass
class DocumentConditionalUpdateRequest:
    primary_key_name: str
    primary_key_value: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
    version_field: str = "version"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentConditionalUpdateRequest":
        return cls(
            primary_key_name=data.get("primary_key_name", "id"),
            primary_key_value=str(data["primary_key_value"]),
            updates=dict(data.get("updates", {})),
            expected_version=data.get("expected_version"),
            version_field=data.get("version_field", "version"),
        )

    def build_update_expression(self):
        names = []
        values: Dict[str, Any] = {}
        parts: List[str] = []
        for idx, (k, v) in enumerate(self.updates.items()):
            name_key = f"#n{idx}"
            value_key = f":v{idx}"
            names.append((name_key, k))
            values[value_key] = v
            parts.append(f"{name_key} = {value_key}")
        expr_names = {k: v for k, v in names}
        if self.expected_version is not None:
            expr_names["#version"] = self.version_field
            values[":expected_version"] = self.expected_version
            parts.append("#version = :expected_version")
        return "SET " + ", ".join(parts), values


@dataclass
class DocumentUpsertResponse:
    ok: bool
    primary_key_name: str
    primary_key_value: str
    document: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return normalize_document(self.__dict__)


@dataclass
class DocumentFetchResponse:
    ok: bool
    document: Optional[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return normalize_document(self.__dict__)


@dataclass
class DocumentQueryResponse:
    ok: bool
    items: List[Dict[str, Any]] = field(default_factory=list)
    count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return normalize_document(self.__dict__)


@dataclass
class DocumentConditionalUpdateResponse:
    ok: bool
    updated_document: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return normalize_document(self.__dict__)
