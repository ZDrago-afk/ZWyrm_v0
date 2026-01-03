import psutil

class ProcessMonitor:
    def snapshot(self):
        processes = []
        for p in psutil.process_iter(['pid', 'name', 'exe', 'username']):
            try:
                processes.append(p.info)
            except psutil.AccessDenied:
                continue
        return processes
