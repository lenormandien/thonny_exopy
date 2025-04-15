# 🧔🏻 thonny_exopy

**Thonny_exopy** est un Plugin pour Thonny conçue pour l'enseignement de la spécialité NSI.
NSI pour récupérer des exercices depuis une API avec aide IA. Ce plugin utilse une API (api_exopy.php) et permet de proposer des exercices typique de la spécialité et propose une aide à la résolution via un prompt spécifique.

![Licence MIT](https://img.shields.io/badge/Licence-MIT-blue.svg)
![Thonny](https://img.shields.io/badge/Thonny-4.1.7+-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.10+-green.svg)

## ✔️ Fonctionnalités principales

** 📋 Navigation dans les exercices

    Récupération de la liste des exercices disponibles par niveau (niveau=1 à 5) via l'API.

    Affichage des titres dans un menu dynamique dans Thonny :

        Menu : Exopy/Niveau X

        Chaque titre appelle la fonction load_exercise(titre, id)

** 📄 Chargement d’un exercice

    À partir d’un identifiant d’exercice, récupération via API :

        de l'énoncé (ENONCE)

        du code de départ (CODE)

        des tests (RES_TEST)

        des contraintes (INTERDIT)

        du niveau (NIVEAU)    

    Création d’un fichier .py dans le dossier temporaire avec :

        Un commentaire d’identification #ID_TITRE

        L'énoncé dans une docstring triple-guillemet

        Le code de départ

** 🤖 Évaluation et feedback pédagogique

    Le bouton "Assistance NSI" :

        Envoie le code de l’élève + les tests + l’énoncé à une API.

        Récupère une analyse pédagogique générée par IA via l'API.

        Affiche le tout dans une fenêtre Tkinter contenant :

            Le feedback IA


## 🔗 Schéma du fonctionnement global du plugin

     ┌──────────────┐
     │   Thonny     │
     │ Éditeur code │───────────────────────────────────────────┐
     └──────┬───────┘                                           |
            ▼                                                   |
      ┌────────────────────┐                                    |
      │ Appel API EXOPY    │                                    |
      │ GET /title         │                                    |
      └─────────┬──────────┘                                    |
                ▼                                               |
       ┌──────────────────────────┐                             |
       │ Menu Thonny Exopy        │                             |
       │ - Niveau 1 à 5           │                             |
       │ - Liste d’exercices      │                             |
       └────────────┬─────────────┘                             |
                    ▼                                           |
          ┌───────────────────────┐                             |
          │ Appel API EXOPY       │                             |
          │ GET /exercice         │                             |
          └───────────┬───────────┘                             |
                      ▼                                         |
            ┌──────────────────────────────┐                    |
            │ Récupération des données :   │                    |
            │  - ENONCE                    │                    |
            │  - CODE                      │                    |
            │  - TESTS                     │                    |
            │  - INTERDIT                  │                    |
            │  - NIVEAU                    │                    |
            └──────────────────────────────┘                    |
                                                                ▼ 
                                                  ┌──────────────────────────────┐
                                                  │ Assistance NSI (bouton)      │
                                                  │   1. Récupère code élève     │
                                                  │   2. Appel API POST feedback │
                                                  │   3. Affiche réponse IA      │
                                                  └──────────────────────────────┘

## 📋 Prérequis

- Thonny 4.1.7 (Python 3.10)
- Connexion internet pour joindre l'API

## 🔗 Dépendances

- tkinter, requests, re, json, tempfile, configparser
- Modules Thonny : get_workbench, get_runner, ui_utils

## 🚀 Installation

Thonny - Ouvrir la console du système
pip install --upgrade pip setuptools wheel
python setup.py sdist bdist_wheel

Thonny - installateur de paquet
Gérer les plugins, installer depuis un fichier local puisvpour trouver et installer le fichier du paquet avec l'extension .whl.

Redémarrer Thonny

## 📁 Structure du projet

```
├── thonnycontrib/                              # Dossier 'plugins' de l'application Thonny
│   ├── exopy/                                  # Dossier de l'application exopy
│   │   ├── __init__.py                         # L'application et le load_plugin() pour Thonny
│   │   ├── config.ini                          # Fichier config de l'application (url de l'API)
│   │   ├── res/                                # Dossier ressources
│   │   │   ├── tools.program_exopy.png         # Logo 16x16 de l'application
│   │   │   ├── tools.program_exopy_2x.png      # Logo 32x32 de l'application

## ⚙️ Configuration

Les paramètres principaux sont configurés dans `config.ini` :

```python
[API]
base_url = https://................../api_exopy.php

[VARIABLES]
enonce = 
code = 
res_test = 	
id_exo = 
titre_exo = 
interdit = 
niveau = 
```


## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.

## 👥 Auteurs et contributeurs

- **Équipe de développement: Moi pour le moment**

- D'après une idée originale de [David Roche](https://www.linkedin.com/in/david-roche-34b9a024a/)
- Développé pour l'Éducation Nationale
  
## 🔗 Liens utiles

- [Thonny]([https://github.com/thonny])

---

Développé pour l'enseignement de la spécialité NSI.
