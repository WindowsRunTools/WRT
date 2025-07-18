import requests
import csv
from io import StringIO
import winreg

REGISTRY_PATH = r"Software\WRT"

def get_latest_version():
    sheet_id = "1c8gg13-GlvBaxH06XiTsfmcyT20Ukdt9Up0ix2JV38E"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

    try:
        response = requests.get(csv_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Erreur lors de la requête :", e)
        return None
    
    content = response.content.decode("utf-8")
    reader = csv.reader(StringIO(content))

    for row in reader:
        if row and row[0].strip():
            return row[0].strip()

    print("Impossible de lire la case A1.")
    return None

def read_registry_value(value_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return value
    except FileNotFoundError:
        return None

def write_registry_value(value_name, value_data):
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
        winreg.CloseKey(key)
    except Exception as e:
        print("Erreur écriture registre :", e)
