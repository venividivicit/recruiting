import logging
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.config import Settings


def setup_logging(settings: "Settings | None" = None) -> None:
    """Configure the ``src`` logger tree: one handler, structured format, env-driven level."""
    from src.core.config import get_settings

    cfg = settings or get_settings()
    level = getattr(logging, cfg.log_level.upper(), logging.INFO)

    src_log = logging.getLogger("src")
    if src_log.handlers:
        src_log.setLevel(level)
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    src_log.addHandler(handler)
    src_log.setLevel(level)
    src_log.propagate = False

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a module logger under the configured ``src`` hierarchy."""
    return logging.getLogger(name)
