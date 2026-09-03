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


def show_system_info():
    info = get_system_info()

    print("\n[SYSTEM INFO]")
    print(f"Platform      : {info['platform']}")
    print(f"Machine       : {info['machine']}")
    print(f"Python        : {info['python']}")
    print(f"Storage total : {info['disk_total_gb']} GB")
    print(f"Storage used  : {info['disk_used_gb']} GB")
    print(f"Storage free  : {info['disk_free_gb']} GB")

    log("System information berhasil dibaca")


def show_logs():
    print("\n[ACTIVITY LOG]")

    if not LOG_FILE.exists():
        print("Belum ada log.")
        return

    content = LOG_FILE.read_text(encoding="utf-8").strip()

    if content:
        print(content)
    else:
        print("Belum ada log.")

    log("Log ditampilkan")


def update_from_github():
    print("\n[GITHUB UPDATE]")
    print("Gunakan perintah berikut dari Termux:")
    print("git pull")

    log("Menu GitHub Update dibuka")


def show_menu():
    print("\n================================")
    print("       TERMUX PROJECT")
    print("================================")
    print("1. System Information")
    print("2. View Logs")
    print("3. GitHub Update")
    print("0. Exit")
    print("================================")


def main():
    log("Program dimulai")

    while True:
        show_menu()

        try:
            choice = input("Pilih menu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nProgram dihentikan.")
            break

        if choice == "1":
            show_system_info()

        elif choice == "2":
            show_logs()

        elif choice == "3":
            update_from_github()

        elif choice == "0":
            log("Program selesai")
            print("Sampai jumpa.")
            break

        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()
