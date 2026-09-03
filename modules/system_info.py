import os
import platform
import shutil


def get_storage_info():
    paths = [
        os.path.expanduser("~"),
        "/data/data/com.termux/files/home",
        "/data/data/com.termux/files/usr",
    ]

    for path in paths:
        try:
            total, used, free = shutil.disk_usage(path)

            return {
                "path": path,
                "total_gb": round(total / (1024 ** 3), 2),
                "used_gb": round(used / (1024 ** 3), 2),
                "free_gb": round(free / (1024 ** 3), 2),
            }

        except (OSError, PermissionError):
            continue

    return {
        "path": None,
        "total_gb": None,
        "used_gb": None,
        "free_gb": None,
    }


def get_system_info():
    storage = get_storage_info()

    return {
        "platform": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "storage_path": storage.get("path"),
        "disk_total_gb": storage.get("total_gb"),
        "disk_used_gb": storage.get("used_gb"),
        "disk_free_gb": storage.get("free_gb"),
    }


if __name__ == "__main__":
    print(get_system_info())
