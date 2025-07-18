import os
import winreg as reg

REGISTRY_PATH = r"Software\WRT"

def find_executable(filename, start_dir="C:\\"):
    for root, dirs, files, in os.walk(start_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None

def save_to_registry(soft_name, exe_path):
    with reg.CreateKey(reg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
        reg.SetValueEx(key, soft_name, 0, reg.REG_SZ, exe_path)
        print(f"[OK] {soft_name} enregistré : {exe_path}")

def scan_and_store_all():
    softwares = {
        "BCU": "BCUninstaller.exe",
        "DiskInfo": "DiskInfo64.exe",
        "Everything": "Everything.exe",
        "OOSU": "OOSU10.exe",
        "KeePass": "KeePassXC.exe",
    }

    for name, exe in softwares.items():
        print(f"🔍 Recherche de {name} ({exe})...")
        path = find_executable(exe)
        if path:
            save_to_registry(name, path)
        else:
            print(f"[!] {name} non trouvé.")

if __name__ == "__main__":
    print("[*] Démarrage du scan dans un Thread.")