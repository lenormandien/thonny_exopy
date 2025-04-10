import tkinter as tk
from tkinter import messagebox
import requests
from thonny import get_workbench


def afficher_exercices():
    url = "https://lenormandien.myqnapcloud.com/exopy_25/backend/api_exopy.php/title?niveau=1"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        titres = [item["titre"] for item in data["titre"]]

        fenetre = tk.Toplevel()
        fenetre.title("Liste des exercices")

        for titre in titres:
            label = tk.Label(fenetre, text=titre.strip())
            label.pack(anchor="w")

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de récupérer les données : {e}")


def ajouter_menu():
    menu = get_workbench().get_menu("view")  # view = "Affichage" en français
    menu.add_command(label="Exercices Exopy", command=afficher_exercices)


def load_plugin():
    ajouter_menu()
