# --------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------MODULES----------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
from tkinter import messagebox
import tkinter as tk
import subprocess
import os
import webbrowser
import threading
import winreg as reg
from pathlib import Path
from urllib.parse import unquote, urlparse
import ctypes
import sys

import Tier
import Messages
import Soft_Chemin
import Link
import CheckUpdate


# --------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------VERSION----------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
REGISTRY_PATH = r"Software\WRT"  # HKEY_CURRENT_USER\SOFTWARE\WRT
VALUE_NAME = "ThemeColor"
VALUE_VERSION = "1.0.0"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    script_path = os.path.abspath(__file__)
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script_path}"', None, 1)
    sys.exit(0)

if not is_admin():
    relaunch_as_admin()

try:
    key = reg.CreateKey(reg.HKEY_CURRENT_USER, REGISTRY_PATH)
    reg.SetValueEx(key, "Version", 0, reg.REG_SZ, VALUE_VERSION) 
    reg.CloseKey(key)
except Exception as e:
    print(f"Erreur : {e}")

# --------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------TKINTER----------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
# Création de la fenêtre principale
root = tk.Tk()
root.geometry('825x600')
root.title("Windows Run Tools")
root.minsize(width=700, height=600)


# icon
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
icon_path = get_resource_path("Image/logowrt.ico")
root.iconbitmap(icon_path)


# FONCTION
# --------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------THEME------------------------------------------------------------ #
# --------------------------------------------------------------------------------------------------------------------- #
def load_theme(): 
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, REGISTRY_PATH)
        value, _ = reg.QueryValueEx(key, VALUE_NAME)
        reg.CloseKey(key)
        return value == 1  
    except FileNotFoundError:
        return False  

def save_theme(is_dark):
    try:
        key = reg.CreateKey(reg.HKEY_CURRENT_USER, REGISTRY_PATH)
        reg.SetValueEx(key, VALUE_NAME, 0, reg.REG_DWORD, 1 if is_dark else 0)
        reg.CloseKey(key)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement dans le registre : {e}")

def toggle_background():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    update_theme()
    save_theme(is_dark_mode)

# Black = 1c1c1c
# White = ececec

def update_theme():
    
    color = "#1c1c1c" if is_dark_mode else "#ececec"
    color_btn = "#5CB2FF"
    text_color = "white" if is_dark_mode else "black"
    inverse_btn = "#1c1c1c" if is_dark_mode else "#ececec"

    # List frames
    frames = [
        root, 
        header_frame, 
        tools_frame, 
        Update_Frame, 
        settings_frame, 
        Tier_frame, 
        Conf_frame, 
        Site_Frame, 
        Logiciel_Frame
    ]

    # Color frames
    for frame in frames:
        frame.configure(bg=color)

    # List Buttons with color
    buttons = [
        btn_tools,
        btn_Tier, 
        btn_settings, 
        btn_politique, 
        btn_site, 
        btn_Logiciel,
        btn_mrt, 
        btn_ntd, 
        btn_Winver, 
        btn_GestionTask,
        btn_GodMode, 
        btn_msinfo, 
        btn_loupe, 
        btn_AppsFolder, 
        btn_RAMMAP,
        btn_DiskInfo,
        btn_BCUninstaller,
        btn_OOSU,
        btn_KeePass,
        button_setting,
        btn_CyberGouv,
        btn_CERT,
        btn_scan,
        btn_show,
        btn_CheckUpdate
        ]

    # List labels with red color
    labels_red = [
        lable_infoWin, 
        label_status, 
        lbl_tier, 
        text_logiciel,
        lbl_version
        ]
    
    btn_interogation = [
        info_CyberGouv,
        info_mrt,
        info_DiskClean,
        info_Winver,
        info_GestionTask,
        info_msinfo,
        info_Loupe,
        info_AppsFolder,
        info_GodMod,
        info_BCU,
        info_DiskInfo,
        info_CERT,
        info_EvrThi,
        info_OOSU,
        info_KeePass,
        ]

    for interogation in btn_interogation:
        interogation.configure(bg=inverse_btn, fg=text_color)
    for button in buttons:
        button.configure(bg=color_btn, fg=text_color)   
    for label in labels_red:
        label.configure(bg=color, fg="red")

    button.configure(bg=color, fg=text_color)

is_dark_mode = load_theme()

# --------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------RESIZE BUTTON------------------------------------------------------ #
# --------------------------------------------------------------------------------------------------------------------- #
resize_after_id = None

def delayed_resize(event=None):
    global resize_after_id
    if resize_after_id:
        root.after_cancel(resize_after_id)
    resize_after_id = root.after(150, resize_button_text)

MIN_WIDTH = 700
MIN_HEIGHT = 600

MIN_SMALL_FONT_SIZE = 8

previous_size = {"width": None, "height": None}
def resize_button_text(event=None):
    global previous_size

    current_width = root.winfo_width()
    current_height = root.winfo_height()

    if previous_size["width"] == current_width and previous_size["height"] == current_height:
        return

    btn_width = btn_GodMode.winfo_width()
    btn_height = btn_GodMode.winfo_height()

    big_size = int(min(btn_height, btn_width) / 3.4)
    small_size = max(int(min(btn_height, btn_width) / 3), MIN_SMALL_FONT_SIZE)

    widgets_with_font = {
        "big": 
        [
            btn_mrt
        ],

        "small": 
        [
            btn_tools,
            btn_Tier,
            btn_settings, 
            btn_politique, 
            btn_site, 
            btn_Logiciel,
            lable_infoWin, 
            label_status, 
            btn_ntd, 
            btn_Winver,
            btn_GestionTask, 
            btn_GodMode, 
            btn_msinfo, 
            btn_loupe, 
            btn_AppsFolder, 
            btn_RAMMAP,
            btn_DiskInfo, 
            btn_BCUninstaller,
            btn_OOSU,
            btn_KeePass, 
            button_setting,  
            lbl_tier, 
            text_logiciel,
            info_CyberGouv,
            btn_CyberGouv,
            info_mrt,
            info_DiskClean,
            info_Winver,
            info_GestionTask,
            info_msinfo,
            info_Loupe,
            info_AppsFolder,
            info_GodMod,
            info_BCU,
            info_DiskInfo,
            info_EvrThi,
            info_CERT,
            btn_CERT,
            lbl_version,
            btn_scan,
            btn_show,
            info_OOSU,
            btn_CheckUpdate
        ]
    }

    for widget in widgets_with_font["big"]:
        widget.config(font=("Arial", big_size))
    for widget in widgets_with_font["small"]:
        widget.config(font=("Arial", small_size))

    previous_size["width"] = current_width
    previous_size["height"] = current_height

# --------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------MESSAGE BOX-------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
# Use Messages.py
def Show_MessageBox(message_key):
    # Check Key
    if message_key in Messages.messages:
        messagebox.showinfo("Information", Messages.messages[message_key])
    else:
        messagebox.showerror("Erreur", "Aucun message trouvé pour cette clé.")

# --------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------TOOLS WINDOWS-------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
def Soft_Tool_Win(chemin_soft):
    def run():
        if chemin_soft in Soft_Chemin.chemin:
            path = Soft_Chemin.chemin[chemin_soft]
            try:
                subprocess.Popen(["explorer.exe", path])
            except Exception as e:
                root.after(0, lambda: messagebox.showerror("Erreur", f"Impossible d’ouvrir le dossier : {e}"))
        else:
            root.after(0, lambda: messagebox.showerror("Erreur", "Une erreur est survenue"))

    threading.Thread(target=run).start()

# --------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------lINK SITE TIER--------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
def Link_Web(LinkWeb):
    if LinkWeb in Link.slink:
        path = Link.slink[LinkWeb]
        webbrowser.open(path)
    else:
        messagebox.showerror("Erreur", "Une erreur est survenue")

# --------------------------------------------------------------------------------------------------------------------- #
# -----------------------------------------------DOWNLOAD TIER--------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
def CheckUpdates():
    def ThreadUpdate():
        btn_CheckUpdate.config(state='disabled')
        latest_version = CheckUpdate.get_latest_version()
        current_version = CheckUpdate.read_registry_value("LastVersion")

        if latest_version is None:
            settings_frame.after(0, lambda: messagebox.showerror("Erreur", "Impossible de vérifier la dernière version."))
            return

        if current_version is None or latest_version != current_version:
            CheckUpdate.write_registry_value("LastVersion", latest_version)
            settings_frame.after(0, lambda: messagebox.showinfo("Scan terminé", f"Une mise à jour est disponible : {latest_version}"))
        else:
            settings_frame.after(0, lambda: messagebox.showinfo("Scan terminé", "Aucune mise à jour disponible."))
        btn_CheckUpdate.config(state='normal')
        
    threading.Thread(target=ThreadUpdate).start()
    


def get_path(soft_name):
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            value, _ = reg.QueryValueEx(key, soft_name)
            return value
    except FileNotFoundError:
        return None


def on_scan_click():
    def run_scan():
        btn_scan.config(state='disabled')
        Tier.scan_and_store_all()
        settings_frame.after(0, lambda: messagebox.showinfo("Scan terminé", "Recherche et enregistrement terminés."))
        btn_scan.config(state='normal')
    threading.Thread(target=run_scan).start()


def show_paths():
    result = ""
    for soft in ["BCU", "DiskInfo", "Everything", "OOSU"]:
        path = get_path(soft)
        result += f"{soft}: {path if path else 'Non trouvé'}\n"
    messagebox.showinfo("Chemins enregistrés", result)

def Download_BCU():
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            exe_path, _ = reg.QueryValueEx(key, "BCU")
    except FileNotFoundError:
        exe_path = None

    if exe_path and os.path.isfile(exe_path):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, None, None, 1)
    else:
        webbrowser.open("https://sourceforge.net/projects/bulk-crap-uninstaller/files/latest/download")

def Cristal_Disk():
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            exe_path, _ = reg.QueryValueEx(key, "DiskInfo")
    except FileNotFoundError:
        exe_path = None

    if exe_path and os.path.isfile(exe_path):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, None, None, 1)
    else:
        webbrowser.open("https://sourceforge.net/projects/bulk-crap-uninstaller/files/latest/download")

def Everything():
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            exe_path, _ = reg.QueryValueEx(key, "Everything")
    except FileNotFoundError:
        exe_path = None

    if exe_path and os.path.isfile(exe_path):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, None, None, 1)
    else:
        webbrowser.open("https://voidtools.com")

def OOSU():
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            exe_path, _ = reg.QueryValueEx(key, "OOSU")
    except FileNotFoundError:
        exe_path = None

    if exe_path and os.path.isfile(exe_path):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, None, None, 1)
    else:
        webbrowser.open("https://www.oo-software.com/fr/shutup10")

def KeePassXC():
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            exe_path, _ = reg.QueryValueEx(key, "KeePass")
    except FileNotFoundError:
        exe_path = None

    if exe_path and os.path.isfile(exe_path):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, None, None, 1)
    else:
        webbrowser.open("https://keepassxc.org/")







# --------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------CREAT GODMOD--------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
def GM_folder():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    godmode_folder_name = "GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}"
    godmode_folder_path = os.path.join(desktop_path, godmode_folder_name)
    
    if not os.path.exists(godmode_folder_path):
        os.makedirs(godmode_folder_path)
        print("Dossier 'GodMode' créé sur le bureau.")
    else:
        print("Le dossier 'GodMode' existe déjà sur le bureau.")

    subprocess.Popen(f'explorer "{godmode_folder_path}"')

# --------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------SELECT FRAME BUTTON---------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
def show_frame(frame):
    frame.tkraise()

# HEADER
header_frame = tk.Frame(root, bg="gray")
header_frame.place(relwidth=1, relheight=0.1)


# Buttons header
btn_tools = tk.Button(header_frame, text="Outils Windows",command=lambda: show_frame(tools_frame))
btn_tools.place(relx=0.02, rely=0.20, relwidth=0.20, height=40)

btn_Tier = tk.Button(header_frame, text="Tiers", command=lambda: show_frame(Tier_frame) )
btn_Tier.place(relx=0.27, rely=0.20, relwidth=0.20, height=40)

btn_settings = tk.Button(header_frame, text="Paramètres", command=lambda: show_frame(settings_frame))
btn_settings.place(relx=0.52, rely=0.20, relwidth=0.20, height=40)

btn_politique = tk.Button(header_frame, text="Politique", command=lambda: Link_Web("WRT"))
btn_politique.place(relx=0.77, rely=0.20, relwidth=0.20, height=40)

# --------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------FRAME SETTING------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
# Creat frames
tools_frame = tk.Frame(root, bg="white")
tools_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

Update_Frame = tk.Frame(root, bg="white")
Update_Frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

settings_frame = tk.Frame(root, bg="white")
settings_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

Tier_frame = tk.Frame(root, bg="white")
Tier_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

Conf_frame = tk.Frame(root, bg="white")
Conf_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

tier_header = tk.Frame(Tier_frame, bg="gray")
tier_header.place(relwidth=0.13, relheight=1)

Site_Frame = tk.Frame(Tier_frame, bg="white")
Site_Frame.place(relx=0.13, rely=0, relwidth=0.87, relheight=1)

Logiciel_Frame = tk.Frame(Tier_frame, bg="white")
Logiciel_Frame.place(relx=0.13, rely=0, relwidth=0.87, relheight=1)

btn_Logiciel = tk.Button(tier_header, text="Logiciels Tier", command=lambda: show_frame(Logiciel_Frame), border=0.5)
btn_Logiciel.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.05)

btn_site = tk.Button(tier_header, text="Sites Tier", command=lambda: show_frame(Site_Frame), border=0.5)
btn_site.place(relx=0.05, rely=0.15, relwidth=0.90, relheight=0.05)

# --------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------TOOLS FRAME------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
# Tool Windows
lable_infoWin = tk.Label(tools_frame, text="Cet outil n'est pas officiel à Windows mais utilise les outils intégrés", fg="red", font=(10))
lable_infoWin.pack(pady=10)

btn_mrt = tk.Button(tools_frame, text="Suppression de\nlogiciel malveillants" ,command=lambda: Soft_Tool_Win("mrt"), borderwidth=0, anchor="center")
btn_mrt.place(relx=0.2, rely=0.12, relwidth=0.115, relheight=0.05)

btn_ntd = tk.Button(tools_frame, text="DiskClean", command=lambda: Soft_Tool_Win("cleanmgr"), borderwidth=0, anchor="center")
btn_ntd.place(relx=0.2, rely=0.24, relwidth=0.115, relheight=0.05)

btn_Winver = tk.Button(tools_frame,text="Ouvrir Winver", command=lambda: Soft_Tool_Win("winver"), borderwidth=0, anchor="center")
btn_Winver.place(relx=0.7, rely=0.12, relwidth=0.115, relheight=0.05)

btn_GestionTask = tk.Button(tools_frame, text="Gestionnaire\ndes tâches", command=lambda: Soft_Tool_Win("Taskmgr"), borderwidth=0, anchor="center")
btn_GestionTask.place(relx=0.7,rely=0.24,relwidth=0.115, relheight=0.05)

btn_GodMode = tk.Button(tools_frame, text="GodMode", command=GM_folder, borderwidth=0, anchor="center")
btn_GodMode.place(relx=0.2,rely=0.36,relwidth=0.115, relheight=0.05)

btn_msinfo = tk.Button(tools_frame, text="Microsoft\ninformation", command=lambda: Soft_Tool_Win("msinfo"), borderwidth=0, anchor="center")
btn_msinfo.place(relx=0.7,rely=0.36,relwidth=0.115, relheight=0.05)

btn_loupe = tk.Button(tools_frame, text="Loupe", command=lambda: Soft_Tool_Win("Magnify"), borderwidth=0, anchor="center")
btn_loupe.place(relx=0.2, rely=0.48,relwidth=0.115, relheight=0.05)

btn_AppsFolder = tk.Button(tools_frame, text="Dossier\nApplications", command=lambda: Soft_Tool_Win("AppFolder"), borderwidth=0, anchor="center")
btn_AppsFolder.place(relx=0.7, rely=0.48, relwidth=0.115, relheight=0.05)


info_mrt = tk.Button(tools_frame,text="❓",command=lambda: Show_MessageBox("btn_mrt"), borderwidth=0,anchor="center")
info_mrt.place(relx=0.32, rely=0.12, relwidth=0.02, relheight=0.03)

info_DiskClean = tk.Button(tools_frame,text="❓",command=lambda: Show_MessageBox("btn_diskclean"), borderwidth=0,anchor="center")
info_DiskClean.place(relx=0.32, rely=0.24, relwidth=0.02, relheight=0.03)

info_Winver = tk.Button(tools_frame,text="❓",command=lambda: Show_MessageBox("btn_winver"), borderwidth=0,anchor="center")
info_Winver.place(relx=0.82, rely=0.12, relwidth=0.02, relheight=0.03)

info_GestionTask = tk.Button(tools_frame, text="❓", command=lambda: Show_MessageBox("btn_gestiontask"), borderwidth=0,anchor="center")
info_GestionTask.place(relx=0.82, rely=0.24, relwidth=0.02, relheight=0.03)

info_msinfo = tk.Button(tools_frame,text="❓",command=lambda: Show_MessageBox("btn_wininfo"), borderwidth=0,anchor="center")
info_msinfo.place(relx=0.82,rely=0.36,relwidth=0.02, relheight=0.03)

info_Loupe = tk.Button(tools_frame, text="❓", command=lambda: Show_MessageBox("btn_loupe"), borderwidth=0,anchor="center")
info_Loupe.place(relx=0.32, rely=0.48, relwidth=0.02, relheight=0.03)

info_AppsFolder = tk.Button(tools_frame, text="❓", command=lambda: Show_MessageBox("btn_AppsFolder"), borderwidth=0,anchor="center")
info_AppsFolder.place(relx=0.82, rely=0.48, relwidth=0.02, relheight=0.03)

info_GodMod = tk.Button(tools_frame,text="❓",command=lambda: Show_MessageBox("btn_GodMod"), borderwidth=0,anchor="center")
info_GodMod.place(relx=0.32, rely=0.36, relwidth=0.02, relheight=0.03)

label_status = tk.Label(tools_frame, text="")
label_status.place(relx=0.9, rely=0.5)

# --------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------SETTING FRAME-------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
button_setting = tk.Button(settings_frame, text="Changer la couleur", command=toggle_background, font=("Arial", 14), borderwidth=0.5)
button_setting.pack(pady=10)

lbl_version = tk.Label(settings_frame, text = f"Version : {VALUE_VERSION}", borderwidth=0.5, anchor="center")
lbl_version.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

btn_scan = tk.Button(settings_frame, text="Rechercher et enregistrer les logiciels", command=on_scan_click)
btn_scan.pack(padx=20, pady=10)

btn_show = tk.Button(settings_frame, text="Afficher les chemins enregistrés", command=show_paths)
btn_show.pack(padx=20, pady=10)

btn_CheckUpdate = tk.Button(settings_frame, text="Vérifier la version de WRT", command=CheckUpdates)
btn_CheckUpdate.pack(padx=20, pady=10)

# --------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------TIER LOGICIEL------------------------------------------------------ #
# --------------------------------------------------------------------------------------------------------------------- #
lbl_tier = tk.Label(Logiciel_Frame, text="Les logiciels présenter disposent différentes versions : gratuite et payante.\n Windows Run Tools n'est pas partenaire avec les logiciels tier.", fg="red", font=(6))
lbl_tier.pack(pady=10)

btn_RAMMAP = tk.Button(Logiciel_Frame, text="EveryThing", command=Everything, bg='#5CB2FF', borderwidth=0, anchor="center")
btn_RAMMAP.place(relx=0.1, rely=0.12, relwidth=0.115, relheight=0.05)

btn_DiskInfo = tk.Button(Logiciel_Frame, text="DiskInfo", command=Cristal_Disk, bg='#5CB2FF', borderwidth=0, anchor="center")
btn_DiskInfo.place(relx=0.4, rely=0.12, relwidth=0.115, relheight=0.05)

btn_BCUninstaller = tk.Button(Logiciel_Frame, text="BCUninstaller", command=Download_BCU, bg='#5CB2FF', borderwidth=0, anchor="center")
btn_BCUninstaller.place(relx=0.7, rely=0.12, relwidth=0.115, relheight=0.05)

btn_OOSU = tk.Button(Logiciel_Frame, text="OOSU", command=OOSU, bg='#5CB2FF', borderwidth=0, anchor="center")
btn_OOSU.place(relx=0.1, rely=0.24, relwidth=0.115, relheight=0.05)

btn_KeePass = tk.Button(Logiciel_Frame, text="KeePassXC", command=KeePassXC, borderwidth=0, anchor="center")
btn_KeePass.place(relx= 0.4, rely=0.24, relwidth=0.115, relheight=0.05)


info_EvrThi = tk.Button(Logiciel_Frame, text="❓", command=lambda: Show_MessageBox("btn_EvrThi"),borderwidth=0, anchor="center")
info_EvrThi.place(relx=0.22, rely=0.12, relwidth=0.02, relheight=0.03)

info_DiskInfo = tk.Button(Logiciel_Frame, text="❓", command=lambda: Show_MessageBox("btn_DiskInfo"),borderwidth=0, anchor="center")
info_DiskInfo.place(relx=0.52, rely=0.12, relwidth=0.02, relheight=0.03)

info_BCU = tk.Button(Logiciel_Frame, text="❓", command=lambda: Show_MessageBox("btn_BCU"),borderwidth=0, anchor="center")
info_BCU.place(relx=0.82, rely=0.12, relwidth=0.02, relheight=0.03)

info_OOSU = tk.Button(Logiciel_Frame, text="❓", command=lambda: Show_MessageBox("btn_OOSU"),borderwidth=0, anchor="center")
info_OOSU.place(relx=0.22, rely=0.24, relwidth=0.02, relheight=0.03)

info_KeePass = tk.Button(Logiciel_Frame, text="❓", command=lambda: Show_MessageBox("btn_KeePass"),borderwidth=0, anchor="center")
info_KeePass.place(relx=0.52, rely=0.24, relwidth=0.02, relheight=0.03)

# --------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------TIER SITE-------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
text_logiciel = tk.Label(Site_Frame, text="Windows Run Tools n'est pas partenaire avec les sites tier.\nJe n'ai pas créé ou participer à la création des sites présenter ici.", fg="red", font=(6))
text_logiciel.pack(pady=10)

btn_CERT = tk.Button(Site_Frame, text="CERT-FR", command=lambda: Link_Web("CERTFR"), bg='#5CB2FF', borderwidth=0, anchor="center")
btn_CERT.place(relx=0.4, rely=0.12, relwidth=0.115, relheight=0.05)

btn_CyberGouv = tk.Button(Site_Frame, text="CyberGouv\nFrance", command=lambda: Link_Web("CMG"), bg='#5CB2FF', borderwidth=0, anchor="center")
btn_CyberGouv.place(relx=0.1, rely=0.12, relwidth=0.115, relheight=0.05)


info_CERT = tk.Button(Site_Frame,text="❓",command=lambda: Show_MessageBox("btn_CERT"),borderwidth=0, anchor="center")
info_CERT.place(relx=0.52, rely=0.12, relwidth=0.02, relheight=0.03)

info_CyberGouv = tk.Button(Site_Frame,text="❓",command=lambda: Show_MessageBox("btn_CyberGouv"),borderwidth=0, anchor="center")
info_CyberGouv.place(relx=0.22, rely=0.12, relwidth=0.02, relheight=0.03)


# --------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------BOUCLE----------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #
root.bind_all('<Configure>', delayed_resize)

show_frame(tools_frame)

update_theme()

root.mainloop()