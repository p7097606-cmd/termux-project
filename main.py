#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import subprocess
import sys

from modules.system_info import get_system_info
from modules.network_info import get_network_info
from modules.device_status import get_device_status


# ========================================
# KONFIGURASI
# ========================================

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "activity.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)


# ========================================
# UTILITAS
# ========================================

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_log(message, show=True):
    line = f"[{get_timestamp()}] {message}"

    try:
        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(line + "\n")
    except OSError as error:
        if show:
            print(f"[LOG ERROR] {error}")

    if show:
        print(line)


def safe_value(value, default="Tidak tersedia"):
    if value is None or value == "":
        return default
    return value


def pause():
    try:
        input("\nTekan ENTER untuk kembali ke menu...")
    except (KeyboardInterrupt, EOFError):
        print()


# ========================================
# DEVICE STATUS
# ========================================

def show_device_status():
    print()
    print("================================")
    print("          DEVICE STATUS")
    print("================================")

    try:
        info = get_device_status()

        print(f"System        : {safe_value(info.get('system'))}")
        print(f"Platform      : {safe_value(info.get('platform'))}")
        print(f"Machine       : {safe_value(info.get('machine'))}")
        print(f"Kernel        : {safe_value(info.get('release'))}")
        print(f"Python        : {safe_value(info.get('python'))}")
        print(f"CPU cores     : {safe_value(info.get('cpu_count'))}")
        print(f"Hostname      : {safe_value(info.get('hostname'))}")

        # RAM
        ram = info.get("ram") or {}

        total_mb = ram.get("total_mb")
        used_mb = ram.get("used_mb")
        available_mb = ram.get("available_mb")

        if total_mb is not None:
            print(f"RAM total     : {total_mb} MB")
            print(f"RAM used      : {safe_value(used_mb)} MB")
            print(f"RAM available : {safe_value(available_mb)} MB")
        else:
            print("RAM           : Tidak tersedia")

        # STORAGE
        storage = info.get("storage") or {}

        total_gb = storage.get("total_gb")
        used_gb = storage.get("used_gb")
        free_gb = storage.get("free_gb")
        storage_path = storage.get("path")

        if total_gb is not None:
            print(f"Storage path  : {safe_value(storage_path)}")
            print(f"Storage total : {total_gb} GB")
            print(f"Storage used  : {safe_value(used_gb)} GB")
            print(f"Storage free  : {safe_value(free_gb)} GB")
        else:
            print("Storage       : Tidak tersedia")

        # UPTIME
        uptime = info.get("uptime")

        if isinstance(uptime, dict):
            days = uptime.get("days")
            hours = uptime.get("hours")
            minutes = uptime.get("minutes")
            raw = uptime.get("raw")

            if (
                days is not None
                and hours is not None
                and minutes is not None
            ):
                print(
                    f"Uptime        : "
                    f"{days} hari, "
                    f"{hours} jam, "
                    f"{minutes} menit"
                )
            elif raw:
                print(f"Uptime        : {raw}")
            else:
                print("Uptime        : Tidak tersedia")
        else:
            print("Uptime        : Tidak tersedia")

        # ANDROID
        android = info.get("android") or {}

        print()
        print("ANDROID")
        print("--------------------------------")

        version = android.get("ro.build.version.release")
        sdk = android.get("ro.build.version.sdk")
        manufacturer = android.get("ro.product.manufacturer")
        model = android.get("ro.product.model")

        print(f"Version       : {safe_value(version)}")
        print(f"SDK           : {safe_value(sdk)}")
        print(f"Manufacturer  : {safe_value(manufacturer)}")
        print(f"Model         : {safe_value(model)}")

        print()
        print(f"Diperiksa     : {safe_value(info.get('timestamp'))}")

        write_log("Device status berhasil diperiksa")

    except Exception as error:
        print(f"\n[ERROR] Gagal membaca device status: {error}")
        write_log(f"ERROR device status: {error}")

    pause()


# ========================================
# SYSTEM INFORMATION
# ========================================

def show_system_info():
    print()
    print("================================")
    print("       SYSTEM INFORMATION")
    print("================================")

    try:
        info = get_system_info()

        print(f"Platform      : {safe_value(info.get('platform'))}")
        print(f"Machine       : {safe_value(info.get('machine'))}")
        print(f"Python        : {safe_value(info.get('python'))}")

        path = info.get("storage_path")
        total = info.get("disk_total_gb")
        used = info.get("disk_used_gb")
        free = info.get("disk_free_gb")

        if total is not None:
            print(f"Storage path  : {safe_value(path)}")
            print(f"Storage total : {total} GB")
            print(f"Storage used  : {safe_value(used)} GB")
            print(f"Storage free  : {safe_value(free)} GB")
        else:
            print("Storage       : Tidak tersedia")

        write_log("System information berhasil dibaca")

    except Exception as error:
        print(f"\n[ERROR] Gagal membaca system information: {error}")
        write_log(f"ERROR system information: {error}")

    pause()


# ========================================
# NETWORK INFORMATION
# ========================================

def show_network_info():
    print()
    print("================================")
    print("        NETWORK INFORMATION")
    print("================================")

    try:
        info = get_network_info()

        print(f"Hostname      : {safe_value(info.get('hostname'))}")
        print(f"Local IP      : {safe_value(info.get('local_ip'), 'Tidak terdeteksi')}")

        internet = info.get("internet")

        if internet is True:
            print("Internet      : TERHUBUNG")
        elif internet is False:
            print("Internet      : TIDAK TERHUBUNG")
        else:
            print("Internet      : TIDAK DIKETAHUI")

        write_log("Network information berhasil diperiksa")

    except Exception as error:
        print(f"\n[ERROR] Gagal membaca network information: {error}")
        write_log(f"ERROR network information: {error}")

    pause()


# ========================================
# VIEW LOGS
# ========================================

def show_logs():
    print()
    print("================================")
    print("          ACTIVITY LOG")
    print("================================")

    try:
        if not LOG_FILE.exists():
            print("Belum ada log.")
            return

        content = LOG_FILE.read_text(
            encoding="utf-8",
            errors="replace"
        ).strip()

        if content:
            print(content)
        else:
            print("Belum ada log.")

    except OSError as error:
        print(f"[ERROR] Tidak dapat membaca log: {error}")

    pause()


# ========================================
# GITHUB UPDATE
# ========================================

def github_update():
    print()
    print("================================")
    print("          GITHUB UPDATE")
    print("================================")
    print("Memeriksa repository...")
    print()

    try:
        # Pastikan direktori memang repository Git.
        check = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=10
        )

        if check.returncode != 0:
            print("[ERROR] Direktori ini bukan repository Git.")
            write_log("ERROR GitHub update: bukan repository Git")
            pause()
            return

        # Ambil update dari GitHub.
        result = subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if stdout:
            print(stdout)

        if stderr:
            print(stderr)

        if result.returncode == 0:
            print()
            print("[OK] GitHub berhasil diperbarui.")
            write_log("GitHub update berhasil")
        else:
            print()
            print("[ERROR] GitHub update gagal.")
            print(f"Exit code : {result.returncode}")

            if stderr:
                print(f"Detail    : {stderr}")

            write_log(
                f"ERROR GitHub update: exit {result.returncode}"
            )

    except FileNotFoundError:
        print("[ERROR] Git tidak ditemukan.")
        print("Pastikan Git sudah terpasang di Termux.")
        write_log("ERROR GitHub update: git tidak ditemukan")

    except subprocess.TimeoutExpired:
        print("[ERROR] GitHub update timeout.")
        print("Koneksi atau repository terlalu lama merespons.")
        write_log("ERROR GitHub update: timeout")

    except KeyboardInterrupt:
        print("\n[INFO] GitHub update dibatalkan.")
        write_log("GitHub update dibatalkan")

    except Exception as error:
        print(f"[ERROR] GitHub update: {error}")
        write_log(f"ERROR GitHub update: {error}")

    pause()


# ========================================
# MENU
# ========================================

def show_menu():
    print()
    print("================================")
    print("         TERMUX PROJECT")
    print("================================")
    print("1. Device Status")
    print("2. System Information")
    print("3. Network Information")
    print("4. View Logs")
    print("5. GitHub Update")
    print("0. Exit")
    print("================================")


def get_choice():
    try:
        return input("Pilih menu: ").strip()
    except KeyboardInterrupt:
        print("\n")
        return "0"
    except EOFError:
        print("\n")
        return "0"


# ========================================
# MAIN LOOP
# ========================================

def main():
    write_log("Program dimulai")

    while True:
        show_menu()

        choice = get_choice()

        if choice == "1":
            show_device_status()

        elif choice == "2":
            show_system_info()

        elif choice == "3":
            show_network_info()

        elif choice == "4":
            show_logs()

        elif choice == "5":
            github_update()

        elif choice == "0":
            write_log("Program selesai")
            print("Sampai jumpa.")
            return 0

        elif choice == "":
            print("\n[ERROR] Pilihan tidak boleh kosong.")
            print("Gunakan angka 0 sampai 5.")

        else:
            print("\n[ERROR] Pilihan tidak valid.")
            print("Gunakan angka 0 sampai 5.")


# ========================================
# ENTRY POINT
# ========================================

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")
        sys.exit(0)
    except Exception as error:
        print(f"\n[FATAL ERROR] {error}")
        sys.exit(1)
