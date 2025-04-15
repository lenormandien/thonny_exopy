# 📚 thonny_exopy

**Thonny_exopy** est un Plugin pour Thonny conçue pour l'enseignement de la spécialité NSI.
NSI pour récupérer des exercices depuis une API avec aide IA. Ce plugin utilse une API (api_exopy.php) et permet de proposer des exercices typique de la spécialité et propose une aide à la résolution via un prompt spécifique.

![Licence MIT](https://img.shields.io/badge/Licence-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-green.svg)
![Thonny](https://img.shields.io/badge/Thonny-4.1.7+-yellow.svg)

## 🚀 Fonctionnalités principales



## 📋 Prérequis

- Thonny 4.1.7 (Python 3.10)
- Connexion internet pour joindre l'API

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

- [Documentation Flask](https://flask.palletsprojects.com/)

---

Développé pour l'enseignement de la spécialité NSI.
