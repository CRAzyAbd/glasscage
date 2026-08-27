import sys
import hashlib
import json
import os
from loguru import logger
from androguard.core.apk import APK

# Silence Androguard's noisy default debug logs
logger.remove()

def get_sha256(file_path):
    """Calculates the SHA-256 hash of a file efficiently by reading in blocks."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def analyze_apk(file_path):
    print(f"\n[*] Analyzing APK: {file_path}")
    try:
        file_hash = get_sha256(file_path)
        apk = APK(file_path)
        
        # Build the structured report dictionary
        report = {
            "sha256": file_hash,
            "app_name": apk.get_app_name(),
            "package_name": apk.get_package(),
            "main_activity": apk.get_main_activity(),
            "permissions": apk.get_permissions() or []
        }
        
        # Print a clean summary to the console
        print(f"[+] SHA-256: {report['sha256']}")
        print(f"[+] App Name: {report['app_name']}")
        print(f"[+] Package: {report['package_name']}")
        print(f"[+] Permissions Found: {len(report['permissions'])}")
        
        # Ensure a 'reports' directory exists and save the JSON
        os.makedirs("reports", exist_ok=True)
        report_path = f"reports/{file_hash}.json"
        
        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)
            
        print(f"\n[+] Structured report successfully saved to {report_path}")
        
    except Exception as e:
        print(f"[-] Error parsing APK: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <path_to_apk>")
        sys.exit(1)
    
    target_apk = sys.argv[1]
    analyze_apk(target_apk)