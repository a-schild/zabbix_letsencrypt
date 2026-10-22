# zabbix_letsencrypt

Zabbix template for letsencrypt certificates monitoring.


## Version 2026-10-22 - security fix, please update
- `cert_check.py` runs as root via sudo and passed its argument through `shell=True`: an argument such as
  `../../../tmp/$(cmd)` together with a planted `cert.pem` executed `cmd` as root. Anyone who can run commands
  as the `zabbix` user (a compromised agent, a local foothold) could become root. The script now accepts only a
  plain lineage name, requires a real directory directly under `/etc/letsencrypt/live` and calls openssl without
  a shell
- `cert_discovery.py` builds its JSON with `json.dumps`; the old string concatenation could leave it unclosed
- `conf/zabbix_letsencrypt` pins both scripts to the arguments the template passes (needs sudo >= 1.9.10, see the
  comment in the file). Replace your existing `/etc/sudoers.d/zabbix_letsencrypt` as well, not only the scripts
- Both scripts use `/usr/bin/python3` explicitly


## Version 2023-01-23
- Convert scripts to python3 - tested with zabbix 6.0.6


## Version 2019-04-30
- Ignore files in cert folder (0.32 certbot puts a readme file in that folder)


## Version 2019-01-22
- Added support to detect certbot version
- Trigger when certbot version below 0.28

## System requirements

- python3
- openssl
- sudo (>= 1.9.10 for the pinned rules in `conf/zabbix_letsencrypt`)
 
## Install

Don't forget change paths:

1. Copy sudo permissions ```install -m 0440 ./zabbix_letsencrypt/conf/zabbix_letsencrypt /etc/sudoers.d/``` and check them with ```visudo -c```

2. Copy scripts: ```cp -r ./zabbix_letsencrypt/scripts/letsencrypt /etc/zabbix/scripts/```

3. Copy zabbix conf: ```cp -r ./zabbix_letsencrypt/conf/letsencrypt.conf /etc/zabbix/zabbix_agent.d/```

4. Restart zabbix agent: ```/etc/init.d/zabbix_agent restart```

5. Import template to Zabbix web.
