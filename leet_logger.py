import logging

"""Leetmail Logger
logger_runs: Run-specific logs, EG, whether a run is successful or not. Should
only include INFO and CRITICAL level logs.
logger_main: Application-specific logs, EG, whether the connection to Leetcode
is successful or not. Should include all levels of logs.
"""

# Base format for all logs
base_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Configure logger for run-specific logs
logger_runs = logging.getLogger("LEETMAIL_RUNS")
logger_runs.setLevel(logging.INFO)

# Console handler for logger_runs
runs_console_handler = logging.StreamHandler()
runs_console_handler.setFormatter(base_format)

# File handler for logger_runs
runs_file_handler = logging.FileHandler("leetmail_runs.log")
runs_file_handler.setFormatter(base_format)

# Add handlers to logger_runs
logger_runs.addHandler(runs_console_handler)
logger_runs.addHandler(runs_file_handler)

# Configure logger for main application logs
logger_main = logging.getLogger("LEETMAIL_APPLICATION")
logger_main.setLevel(logging.DEBUG)

# Console handler for logger_main
main_console_handler = logging.StreamHandler()
main_console_handler.setFormatter(base_format)

# File handler for logger_main
main_file_handler = logging.FileHandler("leetmail.log")
main_file_handler.setFormatter(base_format)

# Add handlers to logger_main
logger_main.addHandler(main_console_handler)
logger_main.addHandler(main_file_handler)

