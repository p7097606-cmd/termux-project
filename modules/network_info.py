import socket
import urllib.request


def get_hostname():
    try:
        return socket.gethostname()
    except Exception:
        return "Tidak tersedia"


def get_local_ip():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        if ip == "127.0.0.1":
            return "Tidak terdeteksi"

        return ip
    except Exception:
        return "Tidak tersedia"


def check_internet():
    try:
        urllib.request.urlopen(
            "https://www.google.com",
            timeout=5
        )
        return True
    except Exception:
        return False


def get_network_info():
    return {
        "hostname": get_hostname(),
        "local_ip": get_local_ip(),
        "internet": check_internet(),
    }
