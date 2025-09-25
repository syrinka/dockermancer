import logging

from autogen_core import EVENT_LOGGER_NAME
from loguru import logger

autogen_level = logger.level("AUTOGEN", no=8, color="<magenta>")


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        logger.opt(exception=record.exc_info).log(
            autogen_level.name,
            record.getMessage().encode().decode("unicode_escape"),
        )


autogen_logger = logging.getLogger(EVENT_LOGGER_NAME)
autogen_logger.setLevel(logging.DEBUG)
autogen_logger.addHandler(InterceptHandler())
logger.debug("Intercept autogen logger")
