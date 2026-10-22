#!/usr/bin/python3
"""Days until the certificate of one certbot lineage expires.

Zabbix item letsencrypt_cert_check[<lineage>], run as root through sudo because
/etc/letsencrypt/live is readable by root only. The argument is therefore untrusted:
only a plain lineage name is accepted, the lineage must be a real directory directly
under /etc/letsencrypt/live, and openssl runs from an argument list, never through a
shell.

Earlier versions appended the argument to a path, checked only os.path.isfile() and
ran the result with shell=True, so an argument such as "../../../tmp/$(cmd)" (with a
planted /tmp/$(cmd)/cert.pem) executed <cmd> as root.

Prints whole days left (0 once expired), or ZBX_NOTSUPPORTED.
"""
import os
import re
import ssl
import subprocess
import sys
import time

LIVE = "/etc/letsencrypt/live"
LINEAGE = re.compile(r"[A-Za-z0-9][A-Za-z0-9.-]{0,252}")


def days_left(name):
    if not LINEAGE.fullmatch(name):
        return None
    lineage = os.path.join(LIVE, name)
    if os.path.islink(lineage) or not os.path.isdir(lineage):
        return None
    cert = os.path.join(lineage, "cert.pem")
    if not os.path.isfile(cert):
        return None
    try:
        out = subprocess.run(["/usr/bin/openssl", "x509", "-enddate", "-noout", "-in", cert],
                             capture_output=True, text=True, timeout=10, check=True,
                             env={"PATH": "/usr/bin:/bin"}).stdout.strip()
        # "notAfter=Jan  2 03:04:05 2027 GMT"
        expires = ssl.cert_time_to_seconds(out.split("=", 1)[1])
    except (OSError, subprocess.SubprocessError, IndexError, ValueError):
        return None
    return max(0, int(round((expires - time.time()) / 86400)))


def main():
    days = days_left(sys.argv[1]) if len(sys.argv) == 2 else None
    print("ZBX_NOTSUPPORTED" if days is None else days)


if __name__ == "__main__":
    main()
