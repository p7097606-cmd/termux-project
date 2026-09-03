from datetime import datetime
from pathlib import Path

from modules.system_info import get_system_info


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

    info = get_system_info()

    print()
    print("[SYSTEM INFO]")
    print(f"Platform      : {info['platform']}")
    print(f"Machine       : {info['machine']}")
    print(f"Python        : {info['python']}")
    print(f"Storage total : {info['disk_total_gb']} GB")
    print(f"Storage used  : {info['disk_used_gb']} GB")
    print(f"Storage free  : {info['disk_free_gb']} GB")

    log("System information berhasil dibaca")
    log("Program selesai")


if __name__ == "__main__":
    main()
