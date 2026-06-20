from app.config import load_all_config
from app.event_logger import EventLogger
from app.session_manager import SessionManager


def main() -> None:
    config = load_all_config()

    logger = EventLogger()
    logger.log_event(
        event_type="app_started",
        metadata={"config_loaded": True},
    )

    session_manager = SessionManager(event_logger=logger)

    # Temporary mocked flow.
    # Later this will come from state_detector.py.
    session_manager.update_state("initial_page", confidence=0.95)
    session_manager.update_state("restart_page", confidence=0.92)
    session_manager.update_state("board_active", confidence=0.97)
    session_manager.update_state("restart_page", confidence=0.91)

    print("Observer skeleton started successfully.")
    print(f"Loaded config keys: {list(config.keys())}")


if __name__ == "__main__":
    main()