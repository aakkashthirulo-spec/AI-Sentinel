SEUIL_SCAN = 4

def detecter_scan_ports(donnees, ip):
    ports = set()
    for log in donnees:
        if log['ip_source'] == ip:
            ports.add(log['port'])

    if len(ports) >= SEUIL_SCAN:
        return (True,f" SCAN DE PORTS ", f"({len(ports)} ports détectés)")

    return (False," Aucun scan de ports")