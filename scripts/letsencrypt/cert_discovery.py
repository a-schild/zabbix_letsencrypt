#!/usr/bin/python3
"""Low-level discovery of certbot lineages (Zabbix item letsencrypt_cert_discovery).

Run as root through sudo, without arguments. Lists every directory under
/etc/letsencrypt/live that holds a cert.pem (certbot also puts a README file there).
The JSON is built with json.dumps; the earlier string concatenation left it unclosed
when the last directory entry was not a certificate.
"""
import json
import os

LIVE = "/etc/letsencrypt/live"


def main():
    try:
        names = sorted(os.listdir(LIVE))
    except OSError:
        names = []
    data = [{"{#DOMAIN}": n} for n in names
            if not os.path.islink(os.path.join(LIVE, n))
            and os.path.isfile(os.path.join(LIVE, n, "cert.pem"))]
    print(json.dumps({"data": data}))


if __name__ == "__main__":
    main()
