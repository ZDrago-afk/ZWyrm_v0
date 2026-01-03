import hashlib

class FileIntegrityMonitor:
    def __init__(self, files):
        self.files = files
        self.baseline = {f: self.hash(f) for f in files}

    def hash(self, path):
        try:
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return None

    def check(self):
        alerts = []
        for f, old in self.baseline.items():
            new = self.hash(f)
            if old and new and old != new:
                alerts.append(f)
        return alerts
