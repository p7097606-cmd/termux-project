from datetime import datetime
from pathlib import Path
import subprocess

from modules.system_info import get_system_info
from modules.network_info import get_network_info


# ========================================
# PATH PROJECT
# ========================================

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "activity.log"

LOG_DIR.mkdir(exist_ok=True)


# ========================================
# LOGGING
# ========================================

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"

    print(line)

    try:
        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(line + "\n")
    except OSError as error:
        print(f"[LOG ERROR] {error}")


# ========================================
# SYSTEM INFORMATION
# ========================================

def show_system_info():
    print("\n================================")
    print("       SYSTEM INFORMATION")
    print("================================")

    try:
        info = get_system_info()

        print(f"Platform      : {info['platform']}")
        print(f"Machine       : {info['machine']}")
        print(f"Python        : {info['python']}")
        print(f"Storage total : {info['disk_total_gb']} GB")
        print(f"Storage used  : {info['disk_used_gb']} GB")
        print(f"Storage free  : {info['disk_free_gb']} GB")

        log("System information berhasil dibaca")

    except Exception as error:
        print(f"[ERROR] Gagal membaca informasi sistem: {error}")
        log(f"ERROR system info: {error}")


# ========================================
# NETWORK INFORMATION
# ========================================

def show_network_info():
    print("\n================================")
    print("        NETWORK INFORMATION")
    print("================================")

    try:
        info = get_network_info()

        print(f"Hostname      : {info['hostname']}")
        print(f"Local IP      : {info['local_ip']}")

        if info["internet"]:
            print("Internet      : TERHUBUNG")
        else:
            print("Internet      : TIDAK TERHUBUNG")

        log("Network information berhasil diperiksa")

    except Exception as error:
        print(f"[ERROR] Gagal membaca informasi jaringan: {error}")
        log(f"ERROR network info: {error}")


# ========================================
# ACTIVITY LOG
# ========================================

def show_logs():
    print("\n================================")
    print("          ACTIVITY LOG")
    print("================================")

    if not LOG_FILE.exists():
        print("Belum ada log.")
        return

    try:
        content = LOG_FILE.read_text(encoding="utf-8").strip()

        if content:
            print(content)
        else:
            print("Belum ada log.")

        log("Log ditampilkan")

    except OSError as error:
        print(f"[ERROR] Tidak dapat membaca log: {error}")


# ========================================
# GITHUB UPDATE
# ========================================

def github_update():
    print("\n================================")
    print("          GITHUB UPDATE")
    print("================================")

    try:
        print("Memeriksa repository...")

        result = subprocess.run(
            ["git", "pull"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.stdout:
            print(result.stdout.strip())

        if result.stderr:
            print(result.stderr.strip())

        if result.returncode == 0:
            print("\n[OK] GitHub berhasil diperbarui.")
            log("GitHub update berhasil")
        else:
            print("\n[ERROR] GitHub update gagal.")
            print(f"Kode keluar: {result.returncode}")
            log(f"ERROR GitHub update: exit {result.returncode}")

    except subprocess.TimeoutExpired:
        print("[ERROR] Git pull timeout.")
        log("ERROR GitHub update: timeout")

    except FileNotFoundError:
        print("[ERROR] Perintah git tidak ditemukan.")
        log("ERROR GitHub update: git tidak ditemukan")

    except Exception as error:
        print(f"[ERROR] {error}")
        log(f"ERROR GitHub update: {error}")


# ========================================
# MENU
# ========================================

def show_menu():
    print("\n================================")
    print("         TERMUX PROJECT")
    print("================================")
    print("1. System Information")
    print("2. Network Information")
    print("3. View Logs")
    print("4. GitHub Update")
    print("0. Exit")
    print("================================")


# ========================================
# MAIN PROGRAM
# ========================================

def main():
    log("Program dimulai")

    while True:
        show_menu()

        try:
            choice = input("Pilih menu: ").strip()

        except KeyboardInterrupt:
            print("\n")
            log("Program dihentikan oleh pengguna")
            break

        except EOFError:
            print("\n")
            log("Input berakhir")
            break

        if choice == "1":
            show_system_info()

        elif choice == "2":
            show_network_info()

        elif choice == "3":
            show_logs()

        elif choice == "4":
            github_update()

        elif choice == "0":
            log("Program selesai")
            print("Sampai jumpa.")
            break

        else:
            print("\n[ERROR] Pilihan tidak valid.")
            print("Gunakan angka 0 sampai 4.")


# ========================================
# PROGRAM ENTRY POINT
# ========================================

if __name__ == "__main__":
    main()
