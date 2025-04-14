import os.path
import tkinter as tk
from tkinter import messagebox
import webbrowser
import requests
import json
from thonny import get_workbench, get_runner
from thonny.ui_utils import select_sequence
import tempfile
import re
import configparser

# Chemin vers le fichier config.ini
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")

# Lecture et écriture dans le fichier config.ini
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# Récupération de l'URL de base de l'API
BASE_URL = config.get("API", "base_url", fallback="https://")


def charger_variables():
    valeurs_defaut = {
        "ENONCE": "",
        "CODE": "",
        "RES_TEST": "",
        "ID_EXO": "",
        "TITRE_EXO": "",
        "INTERDIT": "",
        "NIVEAU": ""
    }
    variables = {}
    if "VARIABLES" not in config:
        config["VARIABLES"] = valeurs_defaut
    for cle, val in valeurs_defaut.items():
        variables[cle] = config.get("VARIABLES", cle, fallback=val)
    return variables

def sauvegarder_variables(variables):
    try:
        if "VARIABLES" not in config:
            config["VARIABLES"] = {}
        for cle, val in variables.items():
            config["VARIABLES"][cle] = val
        with open(CONFIG_PATH, "w", encoding="utf-8") as configfile:
            config.write(configfile)
    except Exception as e:
        messagebox.showinfo("Exopy", f"Erreur de sauvegarde : {e}")

# Chargement :
loaded = charger_variables()
ENONCE = loaded.get("ENONCE", "")
CODE = loaded.get("CODE", "")
RES_TEST = loaded.get("RES_TEST", "")
ID_EXO = loaded.get("ID_EXO", "")
TITRE_EXO = loaded.get("TITRE_EXO", "")
INTERDIT = loaded.get("INTERDIT", "")
NIVEAU = loaded.get("NIVEAU", "")

def _get_current_code():
    editor = get_workbench().get_editor_notebook().get_current_editor()
    if editor is None:
        return None
    return editor.get_code_view().text.get("1.0", "end")

def program_exopy_enabled():
    code = _get_current_code()
    return code is not None and code.strip() != ""

def program_exopy():
    global BASE_URL, ENONCE, CODE, RES_TEST, ID_EXO, TITRE_EXO, INTERDIT, NIVEAU
    
    if not CODE or not _get_current_code().startswith(f'#{ID_EXO}_{TITRE_EXO}'):
        lignes = _get_current_code().strip().splitlines()
        if not lignes:
            messagebox.showinfo("Exopy", "Choisir un exercice Exopy.")
            return

        premiere_ligne = lignes[0].strip()

        # Cherche un motif de type #42_titre_exo
        match = re.match(r"#(\d+)_([\w\d_\-\s]+)", premiere_ligne)
        if match:
            ex_id = match.group(1)
            titre_exo = match.group(2)
            
            # URL de l'API
            url = f"{BASE_URL}/exercice/{ex_id}"
            headers = {'Content-Type': 'application/json'}
            contenu = ""

            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        raw_json = response.json()
                        test_titre = raw_json.get("titre")
                        
                        if titre_exo.strip() == test_titre.strip():
                            ID_EXO = raw_json.get("id", "")
                            TITRE_EXO = raw_json.get("titre", "")
                            ENONCE = raw_json.get("enonce", "")
                            RES_TEST = raw_json.get("test", "")                
                            CODE = raw_json.get("debut_code", "")
                            INTERDIT = raw_json.get("interdit", "")
                            NIVEAU = raw_json.get("niveau", "")
                            
                            # Sauvegarde :
                            mes_variables = {
                                "ENONCE": ENONCE,
                                "CODE": CODE,
                                "RES_TEST": RES_TEST,
                                "ID_EXO": ID_EXO,
                                "TITRE_EXO": TITRE_EXO,
                                "INTERDIT": INTERDIT,
                                "NIVEAU": NIVEAU,
                            }
                            sauvegarder_variables(mes_variables)

                        else:
                            messagebox.showinfo("Exopy", f"Choisir un exercice Exopy. {titre_exo} == {test_titre}")
                            return
                            
                        
                    except ValueError:
                        contenu = "# Erreur : Réponse JSON invalide"
                else:
                    contenu = f"# Erreur HTTP {response.status_code} : {response.text}"
            except requests.exceptions.RequestException as e:
                contenu = f"# Erreur de connexion à l'API : {e}"

        if not _get_current_code().startswith(f'#{ID_EXO}_{TITRE_EXO}'):
            messagebox.showinfo("Exopy", f"Choisir un nouvel exercice Exopy ou le fichier Exopy_{ID_EXO}_{TITRE_EXO}.py")
            return

    # URLs de l'API
    url = f"{BASE_URL}/request"
    
    CODE =  _get_current_code().replace('\n\n"""\n'+ENONCE+'\n"""\n\n',"") #\n\n"""\n{ENONCE}\n"""\n\n

    # Préparation des données à envoyer à l'API
    data = {
        "enonce": ENONCE,
        "code": CODE,
        "res_test": RES_TEST
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            try:
                raw_json = response.json()
                # Récupère uniquement le texte pédagogique
                feedback = raw_json.get("choices", [{}])[0].get("message", {}).get("content", "")
            except ValueError:
                feedback = "Réponse illisible du serveur."
        else:
            feedback = f"Erreur HTTP {response.status_code} : {response.text}"
    except requests.exceptions.RequestException as e:
        feedback = f"Erreur de connexion à l'API : {e}"

    # Création de la fenêtre Tkinter pour afficher un feedback simple
    feedback_window = tk.Toplevel()
    feedback_window.title("Exopy - Assistance NSI")
    feedback_window.geometry("600x400")

    lbl = tk.Label(feedback_window, text="Voici le feedback pédagogique :", font=("Arial", 14))
    lbl.pack(pady=10)

    text_box = tk.Text(feedback_window, wrap=tk.WORD, font=("Courier", 10))
    text_box.insert("1.0", f"Code actuel détecté :\n\n{CODE.strip()[:2048]}\n\n{feedback}")
    text_box.config(state=tk.DISABLED)
    text_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

def test_find_exercise(niveau=1):
    global BASE_URL
    # URLs de l'API
    url = f"{BASE_URL}/title?niveau={niveau}"
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.get(url, headers=headers)
        print(response)  # Debug
        if response.status_code == 200:
            try:
                raw_json = response.json()
                exercises = raw_json.get("titre", [])
                lignes = [f"- {item['titre'].strip()}" for item in raw_json.get("titre", [])]
                feedback = "\n".join(lignes)
            except ValueError:
                feedback = "Réponse illisible du serveur."
        else:
            feedback = f"Erreur HTTP {response.status_code} : {response.text}"
    except requests.exceptions.RequestException as e:
        feedback = f"Erreur de connexion à l'API : {e}"
        
    # Création de la fenêtre Tkinter pour afficher un feedback simple
    feedback_window = tk.Toplevel()
    feedback_window.title("Exopy - Liste des exercices")
    feedback_window.geometry("600x400")

    lbl = tk.Label(feedback_window, text="Voici la liste des exercices :", font=("Arial", 14))
    lbl.pack(pady=10)

    text_box = tk.Text(feedback_window, wrap=tk.WORD, font=("Courier", 10))
    
    text_box.insert("1.0", f"Voici la liste des exercices :\n\n{feedback}")
    
    text_box.config(state=tk.DISABLED)
    text_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            
def find_exercise():
    global BASE_URL
    url = f"{BASE_URL}/title"
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                exercises = data.get("titre", [])
            except ValueError:
                messagebox.showerror("Erreur", "Réponse JSON invalide.")
                return
        else:
            messagebox.showerror("Erreur", f"HTTP {response.status_code} : {response.text}")
            return
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erreur", f"Erreur de connexion à l'API : {e}")
        return

    # Préparation des niveaux
    exercices_par_niveau = {n: [] for n in range(1, 6)}

    for ex in exercises:
        ex_id = ex.get("id")
        if not ex_id:
            continue
        try:
            #niveau = int(test_niveau_exercise_by_id(int(ex_id)))
            niveau = int(ex.get("niveau", 1))
            if 1 <= niveau <= 5:
                exercices_par_niveau[niveau].append(ex)
        except Exception as e:
            print(f"Erreur lors de l'évaluation du niveau pour l'exercice {ex_id} : {e}")
            exercices_par_niveau[1].append(ex)  # Par défaut niveau 1

    # Générer les menus dans Thonny
    for niveau in range(1, 6):
        menu_name = f"Exopy/Niveau {niveau}"
        for ex in exercices_par_niveau[niveau]:
            titre = ex.get("titre", "").strip()
            ex_id = ex.get("id")
            if not ex_id or not titre:
                continue
            
            
            #Utilisation d’un make_handler() pour éviter que toutes les lambdas pointent sur la dernière valeur (piège classique en Python dans une boucle)
            '''def make_handler(titre, ex_id):
                return lambda: load_exercise(titre, ex_id)
            '''
            get_workbench().add_command(
                command_id=f"exopy_ex_{ex_id}",
                menu_name=menu_name,
                command_label=titre,
                handler=load_exercise(titre, ex_id),
                position_in_group="end",
                image=None,
                tester=None,
                group=100 + niveau,
                caption=f"Lancer l'exercice : {titre}",
                include_in_menu=True,
                include_in_toolbar=False,
                bell_when_denied=True,
            )



def load_exercise(titre, ex_id):
    def handler():
        test_find_exercise_by_id(titre, ex_id)
    return handler

def test_find_exercise_by_id(titre, ex_id):
    global BASE_URL, ENONCE, CODE, RES_TEST, ID_EXO, TITRE_EXO, INTERDIT, NIVEAU
    # URL de l'API
    url = f"{BASE_URL}/exercice/{ex_id}"
    headers = {'Content-Type': 'application/json'}
    contenu = ""

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                raw_json = response.json()
                ID_EXO = raw_json.get("id", "")
                TITRE_EXO = raw_json.get("titre", "")
                ENONCE = raw_json.get("enonce", "")
                RES_TEST = raw_json.get("test", "")                
                CODE = raw_json.get("debut_code", "")
                INTERDIT = raw_json.get("interdit", "")
                NIVEAU = raw_json.get("niveau", "")
                
                # Sauvegarde :
                mes_variables = {
                    "ENONCE": ENONCE,
                    "CODE": CODE,
                    "RES_TEST": RES_TEST,
                    "ID_EXO": ID_EXO,
                    "TITRE_EXO": TITRE_EXO,
                    "INTERDIT": INTERDIT,
                    "NIVEAU": NIVEAU,
                }
                sauvegarder_variables(mes_variables)

                contenu = f'#{ID_EXO}_{TITRE_EXO}\n\n"""\n{ENONCE}\n"""\n\n{CODE}\n'
                
                
            except ValueError:
                contenu = "# Erreur : Réponse JSON invalide"
        else:
            contenu = f"# Erreur HTTP {response.status_code} : {response.text}"
    except requests.exceptions.RequestException as e:
        contenu = f"# Erreur de connexion à l'API : {e}"

    # Préparation du nom de fichier
    titre_str = str(titre).replace(" ", "_").replace("\n", "").strip()
    nom_fichier = f"Exopy_{ex_id}_{titre_str}.py"

    # Créer le fichier dans le dossier temporaire
    temp_dir = tempfile.gettempdir()
    chemin_fichier = os.path.join(temp_dir, nom_fichier)

    # Écriture dans le fichier (toujours écrasé à jour)
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        f.write(contenu)

    # Ouvrir le fichier dans l'éditeur Thonny
    get_workbench().get_editor_notebook().show_file(chemin_fichier)

def go_lycee():
    webbrowser.open("https://lycee-tocqueville.fr/")

def _help():
    webbrowser.open("https://lycee-tocqueville.fr/")

def about():
    about_window = tk.Toplevel()
    about_window.title("À propos d'Exopy")
    about_window.geometry("700x300")
    about_window.resizable(False, False)

    tk.Label(
        about_window,
        text="Exopy - Assistance NSI",
        font=("Arial", 14),
        fg="#0055A4"
    ).pack(pady=10)

    info_text = (
        "Version : 1.0.0\n"
        "Développé pour l'enseignement de la NSI en lycée.\n\n"
        "Ce plugin permet de proposer une aide pédagogique structurée\n"
        "et intelligente sur des exercices de programmation Python.\n\n"
        "Auteur : toc-nsi\n"
        "Site : https://lycee-tocqueville.fr/"
    )

    tk.Label(
        about_window,
        text=info_text,
        justify="center",
        font=("Courier", 10)
    ).pack(pady=10)

    tk.Button(
        about_window,
        text="Fermer",
        command=about_window.destroy,
        width=10
    ).pack(pady=15)

def get_commands():
    global session
    MENU_NAME="Exopy"
    commands = {
        23: [
            {
                "command_id": "exopy_issue",
                "menu_name": MENU_NAME,
                "command_label": "Site du Lycée",
                "handler": go_lycee,
                "position_in_group": "end",
                "image": None,
                "tester": None,
                "caption": "Show Help for How to use exopy",
                "include_in_menu": True,
                "include_in_toolbar": False,
                "bell_when_denied": True,
                "enable": lambda: True,
            }
        ],
        24: [
            {
                "command_id": "exopy_about",
                "menu_name": MENU_NAME,
                "command_label": "A propos d'exopy",
                "handler": about,
                "position_in_group": "end",
                "image": None,
                "tester": None,
                "caption": "Learn more about the project",
                "include_in_menu": True,
                "include_in_toolbar": False,
                "bell_when_denied": True,
                "enable": lambda: True,
            },
            {
                "command_id": "exopy_help",
                "menu_name": MENU_NAME,
                "command_label": "Exopy - Assistance NSI",
                "handler": program_exopy,
                "position_in_group": "end",
                "image": None,
                "tester": None,
                "caption": "Exopy - Assistance NSI",
                "include_in_menu": True,
                "include_in_toolbar": False,
                "bell_when_denied": True,
                "enable": lambda: True,
            },
        ],
    }

    return commands

def load_plugin():
    image_path = os.path.join(os.path.dirname(__file__), "res", "tools.program_exopy.png")
    get_workbench().add_command(
        "program_exopy",
        "tools",
        "Exopy - Assistance NSI",
        program_exopy,
        program_exopy_enabled,
        default_sequence=select_sequence("<Control-e>", "<Command-e>"),
        group=120,
        image=image_path,
        caption="Program Exopy",
        include_in_toolbar=True,
    )
    
    find_exercise()
    
    groups = get_commands()

    for group in sorted(groups.keys()):
        for item in groups[group]:
            get_workbench().add_command(
                command_id=item["command_id"],
                menu_name=item["menu_name"],
                command_label=item["command_label"],
                handler=item["handler"],
                position_in_group=item["position_in_group"],
                image=item["image"],
                tester=item["tester"],
                group=group,
                caption=item["caption"],
                include_in_menu=item["include_in_menu"],
                include_in_toolbar=item["include_in_toolbar"],
                bell_when_denied=item["bell_when_denied"],
            )

