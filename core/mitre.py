MITRE_MAP = {
    "suspicious_execution": ("T1059", "Command and Scripting Interpreter"),
    "privilege_escalation": ("T1068", "Exploitation for Privilege Escalation"),
    "file_tampering": ("T1547", "Autostart Execution"),
    "network_anomaly": ("T1071", "Application Layer Protocol")
}

def map_alert(alert):
    return MITRE_MAP.get(alert, ("N/A", "Unknown"))
