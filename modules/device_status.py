import os
import platform
import shutil
import subprocess
import time


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except (OSError, PermissionError):
        return None


def get_ram_info():
    data = read_file("/proc/meminfo")

    if not data:
        return {
            "total_mb": None,
            "available_mb": None,
            "used_mb": None,
        }

    values = {}

    for line in data.splitlines():
        parts = line.split()

        if len(parts) >= 2 and parts[0].endswith(":"):
            try:
                values[parts[0][:-1]] = int(parts[1])
            except ValueError:
                continue

    total = values.get("MemTotal")
    available = values.get("MemAvailable")

    if total is None:
        return {
            "total_mb": None,
            "available_mb": None,
            "used_mb": None,
        }

    if available is None:
        available = values.get("MemFree", 0)

    used = max(total - available, 0)

    return {
        "total_mb": round(total / 1024, 2),
        "available_mb": round(available / 1024, 2),
        "used_mb": round(used / 1024, 2),
    }


def get_storage_info():
    paths = [
        os.path.expanduser("~"),
        "/data/data/com.termux/files/home",
        "/data/data/com.termux/files/usr",
    ]

    result = None

    for path in paths:
        try:
            total, used, free = shutil.disk_usage(path)

            result = {
                "path": path,
                "total_gb": round(total / (1024 ** 3), 2),
                "used_gb": round(used / (1024 ** 3), 2),
                "free_gb": round(free / (1024 ** 3), 2),
            }

            break

        except (OSError, PermissionError):
            continue

    if result is None:
        return {
            "path": None,
            "total_gb": None,
            "used_gb": None,
            "free_gb": None,
        }

    return result


def get_android_version():
    properties = [
        "ro.build.version.release",
        "ro.build.version.sdk",
        "ro.product.model",
        "ro.product.manufacturer",
    ]

    result = {}

    for prop in properties:
        try:
            process = subprocess.run(
                ["getprop", prop],
                capture_output=True,
                text=True,
                timeout=5
            )

            value = process.stdout.strip()

            if value:
                result[prop] = value

        except (OSError, subprocess.SubprocessError):
            result[prop] = None

    return result


def get_uptime():
    # Cara utama: /proc/uptime
    value = read_file("/proc/uptime")

    if value:
        try:
            seconds = float(value.split()[0])

            return {
                "seconds": round(seconds, 2),
                "days": int(seconds // 86400),
                "hours": int((seconds % 86400) // 3600),
                "minutes": int((seconds % 3600) // 60),
            }

        except (ValueError, IndexError):
            pass

    # Fallback: command uptime
    try:
        process = subprocess.run(
            ["uptime"],
            capture_output=True,
            text=True,
            timeout=5
        )

        output = process.stdout.strip()

        if output:
            return {
                "seconds": None,
                "days": None,
                "hours": None,
                "minutes": None,
                "raw": output,
            }

    except (OSError, subprocess.SubprocessError):
        pass

    return None


def get_device_status():
    storage = get_storage_info()
    ram = get_ram_info()
    uptime = get_uptime()
    android = get_android_version()

    return {
        "system": platform.system(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "release": platform.release(),
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "ram": ram,
        "storage": storage,
        "uptime": uptime,
        "android": android,
        "hostname": platform.node(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
