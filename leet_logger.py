import logging

# Configure logger for runs-specific logs
logger_runs = logging.getLogger("leetmail_runs")
logger_runs.setLevel(logging.DEBUG)

# Console handler for logger_runs
runs_console_handler = logging.StreamHandler()
runs_console_handler.setLevel(logging.DEBUG)
runs_console_format = logging.Formatter(
    "%(asctime)s - LEETMAIL_RUNS - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
runs_console_handler.setFormatter(runs_console_format)

# File handler for logger_runs
runs_file_handler = logging.FileHandler("leetmail_runs.log")
runs_file_handler.setLevel(logging.DEBUG)
runs_file_format = logging.Formatter(
    "%(asctime)s - LEETMAIL_RUNS - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
runs_file_handler.setFormatter(runs_file_format)

# Add handlers to logger_runs
logger_runs.addHandler(runs_console_handler)
logger_runs.addHandler(runs_file_handler)

# Configure logger for main application logs
logger_main = logging.getLogger("leetmail")
logger_main.setLevel(logging.DEBUG)

# Console handler for logger_main
main_console_handler = logging.StreamHandler()
main_console_handler.setLevel(logging.DEBUG)
main_console_format = logging.Formatter(
    "%(asctime)s - MAIN - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
main_console_handler.setFormatter(main_console_format)

# File handler for logger_main
main_file_handler = logging.FileHandler("leetmail.log")
main_file_handler.setLevel(logging.DEBUG)
main_file_format = logging.Formatter(
    "%(asctime)s - MAIN - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
main_file_handler.setFormatter(main_file_format)

# Add handlers to logger_main
logger_main.addHandler(main_console_handler)
logger_main.addHandler(main_file_handler)

