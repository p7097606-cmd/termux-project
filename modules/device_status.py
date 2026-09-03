#!/usr/bin/env python3

import os
import platform
import socket
import subprocess
from datetime import datetime

from modules.system_info import get_storage_info


def read_android_property(name):
    """
    Membaca property Android menggunakan getprop.
    """

    try:
        result = subprocess.run(
            ["getprop", name],
            capture_output=True,
            text=True,
            timeout=3,
        )

        if result.returncode == 0:
            value = result.stdout.strip()

            if value:
                return value

    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        pass

    return None


def get_cpu_count():
    try:
        count = os.cpu_count()

        if count is not None:
            return count

    except Exception:
        pass

    return None


def get_ram_info():
    """
    Membaca /proc/meminfo.
    Tidak membutuhkan psutil.
    """

    try:
        values = {}

        with open("/proc/meminfo", "r", encoding="utf-8") as file:
            for line in file:
                parts = line.split()

                if len(parts) >= 2:
                    key = parts[0].rstrip(":")
                    value = parts[1]

                    try:
                        values[key] = int(value)
                    except ValueError:
                        continue

        total_kb = values.get("MemTotal")
        available_kb = values.get("MemAvailable")

        if total_kb is None:
            return {
                "total_mb": None,
                "used_mb": None,
                "available_mb": None,
            }

        if available_kb is None:
            available_kb = values.get("MemFree", 0)

        used_kb = max(total_kb - available_kb, 0)

        return {
            "total_mb": round(total_kb / 1024, 2),
            "used_mb": round(used_kb / 1024, 2),
            "available_mb": round(available_kb / 1024, 2),
        }

    except (OSError, PermissionError):
        return {
            "total_mb": None,
            "used_mb": None,
            "available_mb": None,
        }


def get_uptime():
    """
    Membaca uptime dari /proc/uptime.
    """

    try:
        with open("/proc/uptime", "r", encoding="utf-8") as file:
            first = file.read().split()[0]

        seconds = float(first)

        total_seconds = int(seconds)

        days = total_seconds // 86400
        remaining = total_seconds % 86400

        hours = remaining // 3600
        remaining %= 3600

        minutes = remaining // 60

        return {
            "seconds": total_seconds,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "raw": None,
        }

    except (OSError, PermissionError, ValueError, IndexError):
        pass

    # Fallback ke uptime command
    try:
        result = subprocess.run(
            ["uptime"],
            capture_output=True,
            text=True,
            timeout=3,
        )

        raw = result.stdout.strip()

        if raw:
            return {
                "seconds": None,
                "days": None,
                "hours": None,
                "minutes": None,
                "raw": raw,
            }

    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        pass

    return {
        "seconds": None,
        "days": None,
        "hours": None,
        "minutes": None,
        "raw": None,
    }


def get_kernel():
    """
    Mendapatkan kernel Linux Android sebenarnya.
    """

    try:
        result = subprocess.run(
            ["uname", "-r"],
            capture_output=True,
            text=True,
            timeout=3,
        )

        if result.returncode == 0:
            value = result.stdout.strip()

            if value:
                return value

    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        pass

    try:
        value = platform.uname().release

        if value:
            return value

    except Exception:
        pass

    return None


def get_hostname():
    try:
        hostname = socket.gethostname()

        if hostname:
            return hostname

    except Exception:
        pass

    return "localhost"


def get_device_status():
    android_version = read_android_property(
        "ro.build.version.release"
    )

    sdk_version = read_android_property(
        "ro.build.version.sdk"
    )

    model = read_android_property(
        "ro.product.model"
    )

    manufacturer = read_android_property(
        "ro.product.manufacturer"
    )

    system = platform.system() or "Android"
    machine = platform.machine()
    python_version = platform.python_version()

    kernel = get_kernel()
    cpu_count = get_cpu_count()
    ram = get_ram_info()
    storage = get_storage_info()
    uptime = get_uptime()

    if android_version:
        platform_name = (
            f"Android-{android_version}-"
            f"{machine}-{platform.architecture()[0]}"
        )
    else:
        platform_name = platform.platform()

    return {
        "system": system,
        "platform": platform_name,
        "machine": machine,
        "release": kernel,
        "python": python_version,
        "cpu_count": cpu_count,

        "ram": ram,
        "storage": storage,
        "uptime": uptime,

        "android": {
            "ro.build.version.release": android_version,
            "ro.build.version.sdk": sdk_version,
            "ro.product.model": model,
            "ro.product.manufacturer": manufacturer,
        },

        "hostname": get_hostname(),
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    }


if __name__ == "__main__":
    import pprint

    pprint.pprint(get_device_status())
