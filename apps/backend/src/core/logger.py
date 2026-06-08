import logging
import sys
import os

IS_SHOW_CODE_LINE_NUMBER: bool = True


class ColorFormatter(logging.Formatter):
    LEVEL_COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[41m",  # Red background
    }

    MODULE_COLOR = "\033[35m"
    RESET = "\033[0m"

    def format(self, record):
        file_path = record.pathname
        if "src" in file_path:
            rel_path = (
                file_path.split("src/")[-1].replace(os.sep, ".").replace(".py", "")
            )
        else:
            rel_path = record.module

        if IS_SHOW_CODE_LINE_NUMBER:
            record.where = (
                f"{self.MODULE_COLOR}[{rel_path}:{record.lineno}]{self.RESET}"
            )
        else:
            record.where = f"{self.MODULE_COLOR}[{rel_path}]{self.RESET}"

        levelname = record.levelname
        if levelname in self.LEVEL_COLORS:
            record.levelname = f"{self.LEVEL_COLORS[levelname]}{levelname}{self.RESET}"

        record.asctime = self.formatTime(record, "%H:%M:%S")

        return super().format(record)


logger = logging.getLogger("DanskyiTMA")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

console_formatter = ColorFormatter(
    "%(asctime)s | %(where)s %(levelname)s | %(message)s", datefmt="%H:%M:%S"
)

console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
