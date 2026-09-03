from datetime import datetime
from pathlib import Path
import subprocess

from modules.system_info import get_system_info
from modules.network_info import get_network_info
from modules.device_status import get_device_status


# ========================================
# TERMUX PROJECT
# MAIN APPLICATION
# ========================================

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "activity.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)


# ========================================
# LOGGING
# ========================================

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"

    try:
        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(line + "\n")
    except OSError as error:
        print(f"[LOG ERROR] {error}")

    print(line)


# ========================================
# DEVICE STATUS
# ========================================

def show_device_status():
    print("\n================================")
    print("          DEVICE STATUS")
    print("================================")

    try:
        info = get_device_status()

        print(f"System        : {info.get('system', 'Tidak tersedia')}")
        print(f"Platform      : {info.get('platform', 'Tidak tersedia')}")
        print(f"Machine       : {info.get('machine', 'Tidak tersedia')}")
        print(f"Kernel        : {info.get('release', 'Tidak tersedia')}")
        print(f"Python        : {info.get('python', 'Tidak tersedia')}")
        print(f"CPU cores     : {info.get('cpu_count', 'Tidak tersedia')}")
        print(f"Hostname      : {info.get('hostname', 'Tidak tersedia')}")

        ram = info.get("ram", {})

        if ram.get("total_mb") is not None:
            print(f"RAM total     : {ram['total_mb']} MB")
            print(f"RAM used      : {ram['used_mb']} MB")
            print(f"RAM available : {ram['available_mb']} MB")
        else:
            print("RAM           : Tidak tersedia")

        storage = info.get("storage", {})

        if storage.get("total_gb") is not None:
            print(f"Storage path  : {storage.get('path', 'Tidak tersedia')}")
            print(f"Storage total : {storage['total_gb']} GB")
            print(f"Storage used  : {storage['used_gb']} GB")
            print(f"Storage free  : {storage['free_gb']} GB")
        else:
            print("Storage       : Tidak tersedia")

        uptime = info.get("uptime")

        if uptime:
            if uptime.get("days") is not None:
                print(
                    f"Uptime        : "
                    f"{uptime['days']} hari, "
                    f"{uptime['hours']} jam, "
                    f"{uptime['minutes']} menit"
                )
            elif uptime.get("raw"):
                print(f"Uptime        : {uptime['raw']}")
            else:
                print("Uptime        : Tidak tersedia")
        else:
            print("Uptime        : Tidak tersedia")

        android = info.get("android", {})

        android_version = android.get("ro.build.version.release")
        sdk_version = android.get("ro.build.version.sdk")
        model = android.get("ro.product.model")
        manufacturer = android.get("ro.product.manufacturer")

        print()
        print("ANDROID")
        print("--------------------------------")
        print(f"Version       : {android_version or 'Tidak tersedia'}")
        print(f"SDK           : {sdk_version or 'Tidak tersedia'}")
        print(f"Manufacturer  : {manufacturer or 'Tidak tersedia'}")
        print(f"Model         : {model or 'Tidak tersedia'}")

        print(f"\nDiperiksa     : {info.get('timestamp', 'Tidak tersedia')}")

        log("Device status berhasil diperiksa")

    except Exception as error:
        print(f"[ERROR] Gagal membaca device status: {error}")
        log(f"ERROR device status: {error}")


# ========================================
# SYSTEM INFORMATION
# ========================================

def show_system_info():
    print("\n================================")
    print("       SYSTEM INFORMATION")
    print("================================")

    try:
        info = get_system_info()

        print(f"Platform      : {info.get('platform', 'Tidak tersedia')}")
        print(f"Machine       : {info.get('machine', 'Tidak tersedia')}")
        print(f"Python        : {info.get('python', 'Tidak tersedia')}")
        print(f"Storage total : {info.get('disk_total_gb', 'Tidak tersedia')} GB")
        print(f"Storage used  : {info.get('disk_used_gb', 'Tidak tersedia')} GB")
        print(f"Storage free  : {info.get('disk_free_gb', 'Tidak tersedia')} GB")

        log("System information berhasil dibaca")

    except Exception as error:
        print(f"[ERROR] Gagal membaca system information: {error}")
        log(f"ERROR system information: {error}")


# ========================================
# NETWORK INFORMATION
# ========================================

def show_network_info():
    print("\n================================")
    print("        NETWORK INFORMATION")
    print("================================")

    try:
        info = get_network_info()

        print(f"Hostname      : {info.get('hostname', 'Tidak tersedia')}")
        print(f"Local IP      : {info.get('local_ip', 'Tidak terdeteksi')}")

        if info.get("internet") is True:
            print("Internet      : TERHUBUNG")
        elif info.get("internet") is False:
            print("Internet      : TIDAK TERHUBUNG")
        else:
            print("Internet      : TIDAK DIKETAHUI")

        log("Network information berhasil diperiksa")

    except Exception as error:
        print(f"[ERROR] Gagal membaca network information: {error}")
        log(f"ERROR network information: {error}")


# ========================================
# VIEW LOGS
# ========================================

def show_logs():
    print("\n================================")
    print("          ACTIVITY LOG")
    print("================================")

    if not LOG_FILE.exists():
        print("Belum ada log.")
        log("Log belum tersedia")
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
    print("Memeriksa repository...")

    try:
        result = subprocess.run(
            ["git", "pull"],
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
            print("\n[OK] GitHub berhasil diperbarui.")
            log("GitHub update berhasil")
        else:
            print("\n[ERROR] GitHub update gagal.")
            print(f"Exit code: {result.returncode}")
            log(f"ERROR GitHub update: exit {result.returncode}")

    except FileNotFoundError:
        print("[ERROR] Git tidak ditemukan.")
        log("ERROR GitHub update: git tidak ditemukan")

    except subprocess.TimeoutExpired:
        print("[ERROR] GitHub update timeout.")
        log("ERROR GitHub update: timeout")

    except Exception as error:
        print(f"[ERROR] GitHub update: {error}")
        log(f"ERROR GitHub update: {error}")


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


# ========================================
# MAIN LOOP
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
            log("Program selesai")
            print("Sampai jumpa.")
            break

        else:
            print("\n[ERROR] Pilihan tidak valid.")
            print("Gunakan angka 0 sampai 5.")


# ========================================
# ENTRY POINT
# ========================================

if __name__ == "__main__":
    main()
