from pathlib import Path
from datetime import datetime, timezone
import csv
import json
import uuid


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

EVENTS_CSV_PATH = DATA_DIR / "events.csv"
EVENTS_JSONL_PATH = DATA_DIR / "events.jsonl"
SCORE_LOG_PATH = DATA_DIR / "score_log.csv"


EVENT_FIELDS = [
    "timestamp",
    "event_id",
    "event_type",
    "session_id",
    "game_number",
    "state",
    "detected_object_id",
    "detected_object_name",
    "object_category",
    "expected_score_value",
    "ocr_score",
    "inferred_score",
    "capture_confidence",
    "x",
    "y",
    "screenshot_path",
    "metadata",
]


SCORE_FIELDS = [
    "timestamp",
    "session_id",
    "game_number",
    "ocr_score",
    "inferred_score",
    "score_delta",
    "source",
]


class EventLogger:
    def __init__(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._ensure_csv_headers(EVENTS_CSV_PATH, EVENT_FIELDS)
        self._ensure_csv_headers(SCORE_LOG_PATH, SCORE_FIELDS)

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _ensure_csv_headers(self, path: Path, fields: list[str]) -> None:
        if path.exists():
            return

        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

    def log_event(
        self,
        event_type: str,
        session_id: str | None = None,
        game_number: int | None = None,
        state: str | None = None,
        detected_object_id: str | None = None,
        detected_object_name: str | None = None,
        object_category: str | None = None,
        expected_score_value: int | None = None,
        ocr_score: int | None = None,
        inferred_score: int | None = None,
        capture_confidence: float | None = None,
        x: int | None = None,
        y: int | None = None,
        screenshot_path: str | None = None,
        metadata: dict | None = None,
    ) -> dict:
        event = {
            "timestamp": self._timestamp(),
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "session_id": session_id,
            "game_number": game_number,
            "state": state,
            "detected_object_id": detected_object_id,
            "detected_object_name": detected_object_name,
            "object_category": object_category,
            "expected_score_value": expected_score_value,
            "ocr_score": ocr_score,
            "inferred_score": inferred_score,
            "capture_confidence": capture_confidence,
            "x": x,
            "y": y,
            "screenshot_path": screenshot_path,
            "metadata": json.dumps(metadata or {}),
        }

        self._append_csv(EVENTS_CSV_PATH, EVENT_FIELDS, event)
        self._append_jsonl(EVENTS_JSONL_PATH, event)

        return event

    def log_score(
        self,
        session_id: str | None,
        game_number: int | None,
        ocr_score: int | None,
        inferred_score: int | None,
        score_delta: int | None,
        source: str,
    ) -> dict:
        row = {
            "timestamp": self._timestamp(),
            "session_id": session_id,
            "game_number": game_number,
            "ocr_score": ocr_score,
            "inferred_score": inferred_score,
            "score_delta": score_delta,
            "source": source,
        }

        self._append_csv(SCORE_LOG_PATH, SCORE_FIELDS, row)

        return row

    def _append_csv(self, path: Path, fields: list[str], row: dict) -> None:
        with path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow(row)

    def _append_jsonl(self, path: Path, event: dict) -> None:
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event) + "\n")