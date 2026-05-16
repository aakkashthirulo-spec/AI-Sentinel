PATTERNS_SUSPECTS = [
    # SQL Injection
    "DROP TABLE",
    "SELECT *",
    "UNION SELECT",

    # Path Traversal
    "../",
    "..\\",

    # XSS
    "<SCRIPT>",
    "ALERT(",
    "ONERROR=",

    # Command Injection
    "RM -RF",
    "WGET ",
    "CURL ",
    "/BIN/SH",

    # Exécutables
    ".PHP",
    ".EXE",
    ".SH"
]

def detecter_injections(donnees, ip):
    alertes = []
    for log in donnees:
        if log['ip_source'] != ip:
            continue

        payload = log['payload_texte']
        for pattern in PATTERNS_SUSPECTS:
            if pattern in payload:
                alertes.append(f"❌ SIGNATURE : {pattern}")
    return alertes