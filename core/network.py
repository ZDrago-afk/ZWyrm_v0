import psutil

class NetworkMonitor:
    def __init__(self, ports):
        self.ports = ports

    def scan(self):
        alerts = []
        for c in psutil.net_connections(kind="inet"):
            if c.raddr and c.raddr.port in self.ports:
                alerts.append((c.pid, c.raddr))
        return alerts
