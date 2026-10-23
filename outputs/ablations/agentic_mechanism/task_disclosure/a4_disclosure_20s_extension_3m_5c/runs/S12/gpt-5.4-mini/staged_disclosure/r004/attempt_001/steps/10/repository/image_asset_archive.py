import os
from pathlib import Path
from typing import Iterable, Optional

from google.cloud import storage


def _storage_client() -> storage.Client:
    return storage.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))


def _bucket_name() -> str:
    name = os.getenv("GCS_BUCKET_NAME")
    if not name:
        raise ValueError("GCS_BUCKET_NAME is required")
    return name


def _destination_name(base_prefix: str, source_path: Path, archive_root: Optional[Path]) -> str:
    if archive_root is not None:
        try:
            rel = source_path.resolve().relative_to(archive_root.resolve())
        except Exception:
            rel = source_path.name
    else:
        rel = source_path.name
    return "/".join(part for part in [base_prefix.strip("/"), str(rel).replace(os.sep, "/")] if part)


def archive_image_assets(asset_paths: Iterable[str], caption_text: str, archive_root: Optional[str] = None, prefix: str = "image-analysis") -> list[str]:
    client = _storage_client()
    bucket = client.bucket(_bucket_name())
    archived = []
    root = Path(archive_root).resolve() if archive_root else None

    caption_blob_name = f"{prefix.strip('/')}/captions/derived_caption.txt"
    caption_blob = bucket.blob(caption_blob_name)
    caption_blob.upload_from_string(caption_text, content_type="text/plain; charset=utf-8")
    archived.append(caption_blob_name)

    for asset in asset_paths:
        src = Path(asset)
        if not src.is_file():
            continue
        blob_name = _destination_name(f"{prefix.strip('/')}/artifacts", src, root)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(str(src))
        archived.append(blob_name)

    return archived


def archive_directory(directory: str, caption_text: str, prefix: str = "image-analysis") -> list[str]:
    dir_path = Path(directory)
    files = [str(p) for p in dir_path.rglob("*") if p.is_file()]
    return archive_image_assets(files, caption_text, archive_root=str(dir_path), prefix=prefix)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("caption")
    parser.add_argument("--prefix", default="image-analysis")
    args = parser.parse_args()
    print("
".join(archive_directory(args.directory, args.caption, prefix=args.prefix)))
