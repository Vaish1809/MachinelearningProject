import logging #- This imports Python’s standard **logging module**, which lets you record messages (like errors, warnings, info, etc.) to files or the console
import os  #This gives access to operating system functions, like creating folders, joining paths, etc.
from datetime import datetime #This imports the `datetime` class to **get the current date and time**.

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #This creates a log file name based on the current date and time, formatted as `month_day_year_hour_minute_second.log`.
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE) #cwd - /home/vaishnavi/myproject/ - create folder = logs , append file - /06_18_2025_16_22_10.log
os.makedirs(logs_path, exist_ok=True) #This creates a directory for logs if it doesn't already exist. `exist_ok=True` means it won't raise an error if the directory already exists.

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
if __name__ == "__main__":
    logging.info("Logging has started")  #This logs an info message indicating that logging has started. This is useful for debugging and tracking the flow of the program.
    print(f"Logs are saved at {LOG_FILE_PATH}")  #This prints the path where the log file is saved, so you can easily find it.