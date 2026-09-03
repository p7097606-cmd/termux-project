#!/usr/bin/env python3

import socket
import subprocess


def get_hostname():
    try:
        hostname = socket.gethostname()

        if hostname:
            return hostname

    except Exception:
        pass

    return "localhost"


def get_local_ip():
    """
    Mencoba beberapa metode untuk mendapatkan IP lokal.
    Tidak membutuhkan root.
    """

    # Metode 1: Android/Linux `ip`
    try:
        result = subprocess.run(
            ["ip", "-4", "-o", "addr", "show", "scope", "global"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            for line in result.stdout.splitlines():
                parts = line.split()

                for index, value in enumerate(parts):
                    if value == "inet" and index + 1 < len(parts):
                        address = parts[index + 1].split("/")[0]

                        if address and not address.startswith("127."):
                            return address

    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        pass

    # Metode 2: koneksi UDP tanpa mengirim paket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)

        try:
            sock.connect(("8.8.8.8", 80))
            address = sock.getsockname()[0]

            if address and not address.startswith("127."):
                return address

        finally:
            sock.close()

    except (OSError, socket.error):
        pass

    # Metode 3: hostname resolution
    try:
        addresses = socket.getaddrinfo(
            socket.gethostname(),
            None,
            socket.AF_INET,
        )

        for item in addresses:
            address = item[4][0]

            if address and not address.startswith("127."):
                return address

    except (OSError, socket.error):
        pass

    return None


def check_internet():
    """
    Memeriksa konektivitas internet dengan DNS socket.
    """

    hosts = [
        ("1.1.1.1", 53),
        ("8.8.8.8", 53),
    ]

    for host, port in hosts:
        try:
            sock = socket.create_connection(
                (host, port),
                timeout=3,
            )
            sock.close()
            return True

        except (OSError, socket.error):
            continue

    return False


def get_network_info():
    hostname = get_hostname()
    local_ip = get_local_ip()
    internet = check_internet()

    return {
        "hostname": hostname,
        "local_ip": local_ip or "Tidak terdeteksi",
        "internet": internet,
    }


if __name__ == "__main__":
    print(get_network_info())
