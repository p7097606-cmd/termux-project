from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "activity.log"


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"

    print(line)

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(line + "\n")


def main():
    print("================================")
    print("       TERMUX PROJECT")
    print("================================")

    log("Program dimulai")
    log("Python berjalan dengan normal")
    log("GitHub + Termux project aktif")
    log("Program selesai")


if __name__ == "__main__":
    main()
