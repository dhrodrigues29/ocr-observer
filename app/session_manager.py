from dataclasses import dataclass
from datetime import datetime, timezone
import uuid

from app.event_logger import EventLogger


VALID_STATES = {
    "unknown",
    "initial_page",
    "restart_page",
    "board_active",
}


@dataclass
class GameSession:
    session_id: str
    game_number: int
    started_at: str
    ended_at: str | None = None
    inferred_score: int = 0
    ocr_score: int | None = None
    active: bool = True


class SessionManager:
    def __init__(self, event_logger: EventLogger) -> None:
        self.event_logger = event_logger
        self.current_state = "unknown"
        self.previous_state = "unknown"
        self.current_session: GameSession | None = None
        self.game_number = 0

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def update_state(self, new_state: str, confidence: float | None = None) -> None:
        if new_state not in VALID_STATES:
            new_state = "unknown"

        if new_state == self.current_state:
            return

        self.previous_state = self.current_state
        self.current_state = new_state

        self._log_state_detection(new_state, confidence)
        self._handle_transition(self.previous_state, self.current_state)

    def _log_state_detection(self, state: str, confidence: float | None) -> None:
        event_by_state = {
            "initial_page": "initial_page_detected",
            "restart_page": "restart_page_detected",
            "board_active": "board_detected",
            "unknown": "unknown_state",
        }

        self.event_logger.log_event(
            event_type=event_by_state[state],
            session_id=self.current_session.session_id if self.current_session else None,
            game_number=self.game_number,
            state=state,
            capture_confidence=confidence,
        )

    def _handle_transition(self, previous: str, current: str) -> None:
        if current == "board_active" and previous in {"initial_page", "restart_page"}:
            self.start_game()

        if previous == "board_active" and current in {"initial_page", "restart_page"}:
            self.end_game(reason=f"transition_to_{current}")

    def start_game(self) -> GameSession:
        self.game_number += 1

        self.current_session = GameSession(
            session_id=str(uuid.uuid4()),
            game_number=self.game_number,
            started_at=self._timestamp(),
        )

        self.event_logger.log_event(
            event_type="game_started",
            session_id=self.current_session.session_id,
            game_number=self.game_number,
            state=self.current_state,
            inferred_score=self.current_session.inferred_score,
            ocr_score=self.current_session.ocr_score,
        )

        return self.current_session

    def end_game(self, reason: str) -> None:
        if not self.current_session:
            return

        self.current_session.active = False
        self.current_session.ended_at = self._timestamp()

        self.event_logger.log_event(
            event_type="game_ended",
            session_id=self.current_session.session_id,
            game_number=self.current_session.game_number,
            state=self.current_state,
            inferred_score=self.current_session.inferred_score,
            ocr_score=self.current_session.ocr_score,
            metadata={"reason": reason},
        )

        self.current_session = None

    def get_current_session_id(self) -> str | None:
        if not self.current_session:
            return None

        return self.current_session.session_id