import platform
import shutil


def get_system_info():
    total, used, free = shutil.disk_usage("/")

    return {
        "platform": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "disk_total_gb": round(total / (1024 ** 3), 2),
        "disk_used_gb": round(used / (1024 ** 3), 2),
        "disk_free_gb": round(free / (1024 ** 3), 2),
    }
