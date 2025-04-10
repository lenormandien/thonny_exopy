"""
pip install -e .
Le . signifie "ici" → c’est indispensable quand tu installes un projet local.
"""
from setuptools import setup
import os
import sys

# Détection du répertoire où Thonny est installé
def get_thonny_plugin_dir():
    thonny_path = os.path.dirname(os.path.abspath(sys.argv[0]))  # Récupère le chemin actuel du script
    if sys.platform == "win32":
        plugin_dir = os.path.join(os.environ['APPDATA'], "Python", "Python310", "site-packages", "thonny", "plugins")
    else:
        plugin_dir = os.path.expanduser("~/.local/lib/python3.10/site-packages/thonny/plugins")

    # Convertir les backslashes en forward slashes pour éviter les problèmes d'échappement
    return plugin_dir.replace("\\", "/")

# Le répertoire de plugin pour Thonny
plugin_dir = get_thonny_plugin_dir()
print(plugin_dir)

setup(
    name='thonny_exopy',
    version='0.1',
    description='Plugin Thonny NSI pour récupérer des exercices depuis une API avec aide IA',
    py_modules=['thonnyplugin'],  # Un seul fichier python
    install_requires=[
        'thonny>=4.1.4',
        'requests>=2.27.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    entry_points={
        'thonny.plugins': [
            'exopy = thonnyplugin'
        ]
    },
    # Cibler automatiquement le dossier des plugins de Thonny
    options={
        'install': {
            'install_lib': plugin_dir
        }
    }
)

