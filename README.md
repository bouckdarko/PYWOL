
# PyWoL

PyWoL est une application Python avec une interface graphique (GUI) permettant de gérer et d'utiliser la fonctionnalité Wake-on-LAN (WoL) pour réveiller des périphériques sur le réseau local.

## Fonctionnalités

- **Réveiller des périphériques** en utilisant leur adresse MAC.
- **Ajouter, supprimer et gérer** une liste de périphériques enregistrés.
- **Interface utilisateur personnalisable** avec prise en charge des thèmes clair et sombre.
- **Couleur d'accentuation configurable** pour personnaliser l'apparence de l'application.
- **Authentification sécurisée** avec protection par mot de passe.
- **Gestion des paramètres** pour modifier le thème, la couleur d'accentuation et le mot de passe.
- **Barre de titre personnalisée** avec des icônes adaptatives en SVG.
- **Notification** lorsque le périphérique est réveillé et accessible.

## Prérequis

- **Python 3.8+**
- **PySide6**
- **bcrypt**

## Installation

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/bouckdarko/pywol.git
   cd pywol
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé) :**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Sous Windows : venv\Scripts\activate
   ```

3. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Lancement de l'application

```bash
python pywol.py
```

### Fonctionnalités principales

- **Ajouter un périphérique :** Permet d'enregistrer un nouveau périphérique avec son nom, adresse MAC et adresse IP.
- **Réveiller un périphérique :** Envoie un paquet WoL pour réveiller le périphérique sélectionné.
- **Modifier les paramètres :** Accédez aux paramètres pour changer le thème, la couleur d'accentuation et le mot de passe.
- **Authentification :** À l'ouverture de l'application, si un mot de passe est défini, une demande d'authentification est affichée.

## Empaquetage avec PyInstaller

Pour distribuer l'application sous forme exécutable, vous pouvez utiliser PyInstaller avec le fichier `.spec` fourni.

pyinstaller pywol.spec

L'exécutable sera généré dans le dossier `dist/`.

## Configuration

### Thème et couleur d'accentuation

Vous pouvez choisir entre un thème clair et un thème sombre.  
La couleur d'accentuation est utilisée pour les boutons, les bordures et les icônes SVG. Vous pouvez la personnaliser dans les paramètres.

### Sécurité

L'application utilise `bcrypt` pour hacher et vérifier les mots de passe.  
Il est recommandé de définir un mot de passe pour sécuriser l'accès à l'application.

## Structure du projet

- `pywol.py` : Point d'entrée principal de l'application.
- `gui/` : Contient les fichiers liés à l'interface utilisateur.
  - `main_window.py` : Fenêtre principale de l'application.
  - `settings_window.py` : Fenêtre des paramètres.
  - `theme_manager.py` : Gestion des thèmes et des styles.
- `widgets/` : Contient les widgets personnalisés.
- `auth/` : Gestion de l'authentification.
- `database/` : Gestion des données et des paramètres.
- `api/` : Contient les fonctions liées au Wake-on-LAN.
- `assets/` : Contient les ressources telles que les icônes SVG.

## Dépendances

Liste des principales dépendances :

- `PySide6`
- `bcrypt`

Vous pouvez installer toutes les dépendances avec :

pip install -r requirements.txt

## Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des issues ou des pull requests pour améliorer l'application.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
