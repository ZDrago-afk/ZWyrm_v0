import yaml
import time
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.monitor import ProcessMonitor
from core.detector import Detector
from core.responder import Responder
from core.logger import setup_logger
from core.fim import FileIntegrityMonitor
from core.network import NetworkMonitor

class ZWyrmEngine:
    def __init__(self):
        # Try multiple possible config locations
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        possible_config_paths = [
            os.path.join(project_root, "config", "zwyrm.yaml"),
            os.path.join(project_root, "zwyrm.yaml"),
            "/etc/zwyrm/zwyrm.yaml",
            os.path.expanduser("~/.config/zwyrm/zwyrm.yaml"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "zwyrm.yaml")
        ]
        
        config_path = None
        for path in possible_config_paths:
            if os.path.exists(path):
                config_path = path
                break
        
        if not config_path:
            print("[!] No config file found. Creating default...")
            # Use the first path as default
            config_path = possible_config_paths[0]
            self.create_default_config(config_path)
        
        print(f"[*] Loading config from: {config_path}")
        
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        self.logger = setup_logger()
        self.process_monitor = ProcessMonitor()
        self.detector = Detector()
        self.responder = Responder(self.config.get("mode", "safe"))
        
        # Initialize FIM if configured
        if "file_integrity" in self.config:
            watch_files = self.config["file_integrity"].get("watch", [])
            self.fim = FileIntegrityMonitor(watch_files)
        else:
            self.fim = None
            
        # Initialize Network monitor if configured
        if "network" in self.config:
            ports = self.config["network"].get("suspicious_ports", [])
            self.net_monitor = NetworkMonitor(ports)
        else:
            self.net_monitor = None
    
    def create_default_config(self, config_path):
        """Create a default config file if not found"""
        default_config = {
            "mode": "safe",
            "logging": {
                "level": "INFO",
                "file": "/var/log/zwyrm/zwyrm.log",
                "max_size": 10485760,
                "backup_count": 5
            },
            "file_integrity": {
                "watch": [
                    "/etc/passwd",
                    "/etc/shadow",
                    "/etc/ssh/sshd_config",
                    "/etc/sudoers",
                    "/etc/hosts"
                ],
                "check_interval": 60
            },
            "network": {
                "suspicious_ports": [4444, 1337, 6666, 31337, 31338],
                "monitor_outgoing": True,
                "monitor_incoming": True
            },
            "process": {
                "scan_interval": 3,
                "whitelist": [
                    "/usr/bin/python3",
                    "/bin/bash",
                    "/usr/bin/sudo"
                ]
            },
            "alerting": {
                "email": {
                    "enabled": False,
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "sender": "zwyrm@localhost",
                    "recipients": []
                },
                "slack": {
                    "enabled": False,
                    "webhook_url": ""
                }
            }
        }
        
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        print(f"[+] Created default config at: {config_path}")
    
    def run(self):
        self.logger.info("ZWyrm Engine started")
        print("[+] ZWyrm is running. Press Ctrl+C to stop.")
        
        try:
            while True:
                self.check_processes()
                if self.fim:
                    self.check_files()
                if self.net_monitor:
                    self.check_network()
                time.sleep(3)
        except KeyboardInterrupt:
            self.logger.info("ZWyrm stopped by user")
    
    def check_processes(self):
        processes = self.process_monitor.snapshot()
        for proc in processes:
            alerts = self.detector.analyze(proc)
            for alert_name, mitre_info in alerts:
                self.logger.warning(f"Alert: {alert_name} | MITRE: {mitre_info}")
                if proc.get("pid"):
                    action = self.responder.act(proc["pid"])
                    self.logger.info(f"Response: {action}")
    
    def check_files(self):
        altered = self.fim.check()
        for f in altered:
            self.logger.warning(f"File modified: {f} | MITRE: T1547")
    
    def check_network(self):
        suspicious = self.net_monitor.scan()
        for pid, addr in suspicious:
            self.logger.warning(f"Suspicious connection from PID {pid} to {addr}")