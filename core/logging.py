import logging

from autogen_core import EVENT_LOGGER_NAME
from loguru import logger

from core.config import config

chat_level = logger.level("CHAT", no=8, color="<cyan>")
autogen_level = logger.level("AUTOGEN", no=6, color="<magenta>")


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        logger.opt(exception=record.exc_info).log(
            autogen_level.name,
            record.getMessage(),
        )


autogen_logger = logging.getLogger(EVENT_LOGGER_NAME)
autogen_logger.setLevel(logging.DEBUG)
autogen_logger.addHandler(InterceptHandler())
logger.debug("Intercept autogen logger")

if config.chat.logging:
    logger.add(
        "chat.log",
        level="CHAT",
        format="{time} {message}",
        filter=lambda r: r["level"].name == "CHAT",
    )
