from core.mitre import map_alert

SUSPICIOUS_PATHS = ["/tmp", "/var/tmp", "/dev/shm"]

class Detector:
    def analyze(self, proc):
        alerts = []
        exe = proc.get("exe") or ""
        user = proc.get("username")

        if any(exe.startswith(p) for p in SUSPICIOUS_PATHS):
            alerts.append("suspicious_execution")

        if user == "root" and exe.startswith("/home"):
            alerts.append("privilege_escalation")

        return [(a, map_alert(a)) for a in alerts]
