"""Create shareable audit metadata without copying the full local source archive."""
from argparse import ArgumentParser
from pathlib import Path
import csv
import hashlib
import json

SITES = ("kr", "en", "jp", "cn", "tw")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(source: Path) -> list[dict[str, object]]:
    files: list[Path] = []
    for site in SITES:
        files.extend((source / "pages" / site).glob("*.json"))
        files.extend((source / "pages" / site).glob("*.html.gz"))
        files.extend(path for path in (source / "evidence" / site).glob("*") if path.is_file())
    files.extend(path for path in (source / "review" / "rendered_code").glob("*") if path.is_file())
    return [
        {
            "relative_path": path.relative_to(source).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "stored_in_repository": "no",
        }
        for path in sorted(set(files))
    ]


def write_outputs(source: Path, repository: Path) -> None:
    data_dir = repository / "audit" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    extra = json.loads((source / "extra_validation.json").read_text(encoding="utf-8"))
    allowed = ("site", "requested", "url", "status", "canonical")
    validated = [{key: item.get(key) for key in allowed} for item in extra]
    (data_dir / "validated-urls.json").write_text(
        json.dumps(validated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    rows = build_manifest(source)
    with (data_dir / "source-evidence-manifest.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"validated_urls": len(validated), "manifest_files": len(rows)}, ensure_ascii=False))


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("source_audit", type=Path)
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()
    write_outputs(args.source_audit.resolve(), args.repository.resolve())


if __name__ == "__main__":
    main()
