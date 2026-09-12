import platform
import subprocess
import os
import shutil


# script qui recup le mot de passe wifi actif sur win et linux


def get_platform() -> str:
    print("===DETECTION DE L'OS===")
    print("OS : ", str(platform.system()))
    print("===DETECTION DE L'OS TERMINEE===")
    return platform.system()

# récupérer le wifi sur lequel la machine est connectée selon si c'est windows ou linux avec la commande appropriée
# return le nom de ce wifi en str
def get_active_wifi() -> str:
    print("===RECUPERATION DU WIFI ACTIF===")

    os_name = platform.system()
    wifi_name = ""

    if os_name == "Linux":
        cmd = ["nmcli", "-t", "-f", "NAME", "connection", "show", "--active"]
        print(" ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)
        wifi_name = result.stdout.strip().splitlines()[0] if result.stdout.strip() else ""

    elif os_name == "Windows":
        cmd = ["netsh", "wlan", "show", "interfaces"]
        print(" ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)
        for ligne in result.stdout.splitlines():
            if "SSID" in ligne and "BSSID" not in ligne:
                wifi_name = ligne.split(":", 1)[1].strip()
                break

    print("==> wifi actif: ", wifi_name)
    print("===RECUPERATION DU WIFI ACTIF TERMINEE===")
    return wifi_name





def show_networks_win():
    print("===AFFICHAGE DES RESEAUX WIFI DETECTE===")
    cmd = ["netsh", "wlan", "show", "profiles"]
    print(" ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print("===AFFICHAGE TERMINE===")


# Récupérer le mot de passe du wifi
# return le mot de passe en string
def get_pass_win() -> str:
    print("===RECUPERATION DU MOT DE PASSE DU RESEAU===")
    wifi_name: str = get_active_wifi()
    cmd = ["netsh", "wlan", "show", "profile", f"name={wifi_name}", "key=clear"]
    print(" ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)
    mdp = ""
    for ligne in result.stdout.splitlines():
        if "Contenu de la clé" in ligne or "Key Content" in ligne:
            mdp = ligne.split(":", 1)[1].strip()
            break

    print("===RECUPERATION TERMINEE===")
    return mdp







# Afficher et récupérer tous les réseaux wifi détectés
def show_networks_lin():
    print("===AFFICHAGE DES RESEAUX WIFI DETECTE===")
    cmd = ["nmcli", "connection", "show"]
    print(" ".join(cmd))
    # capture_output=True évite que nmcli détecte un vrai terminal et
    # ouvre un pager (less) qui bloquerait le script en attente de touche
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print("===AFFICHAGE TERMINE===")


# Récupérer mot de passe wifi du réseau auquel la machine linux est connectée
# return le mdp en string
def get_pass_lin() -> str:
    print("===RECUPERATION DU MOT DE PASSE DU RESEAU===")
    wifi_name: str = get_active_wifi()
    cmd = ["sudo", "nmcli", "--show-secrets", "-g",
           "802-11-wireless-security.psk", "connection", "show", wifi_name]
    print(" ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)
    mdp = result.stdout.strip()

    print("===RECUPERATION TERMINEE===")
    return mdp








# Détecter OS de la machine : Linux ou Windows
# Afficher tous les réseaux détectés avec show_networks()
# Afficher le mot de passe du réseau auquel la machine est connectée avec get_pass()
def start():
    print("======DEMMARAGE DU PROGRAMME======")
    mdp: str = ""

    print("==> éxécution de la détection d'OS")
    os_name = get_platform()

    if os_name == "Linux":
        print("==> éxécution de la récupération des réseaux")
        show_networks_lin()
        print("===> éxécution de la récupération du mot de passe du réseau : ")
        mdp = get_pass_lin()

    if os_name == "Windows":
        print("==> éxécution de la récupération des réseaux")
        show_networks_win()
        print("===> éxécution de la récupération du mot de passe du réseau : ")
        mdp = get_pass_win()

    print("==> Mot de passe trouvé: ", mdp)
    print("======FIN DU PROGRAMME======")


start()