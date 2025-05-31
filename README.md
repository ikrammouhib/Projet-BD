# 🎓 Projet Bases de Données - Gestion Hôtelière

## Description

Ce projet a été réalisé dans le cadre du module **Bases de Données Relationnelles** (Licence MIP, Semestre 4) à la **Faculté des Sciences Semlalia - Université Cadi Ayyad**.  
L’objectif est de concevoir et exploiter une **base de données complète** pour un groupe hôtelier, tout en développant une **interface web interactive** permettant la gestion :

- Des clients
- Des réservations
- Des chambres
- Des services
- Des évaluations

Une attention particulière a été portée à la **modélisation conceptuelle et logique** de la base, ainsi qu’à l’ergonomie de l’interface utilisateur.

---

## Binôme

- **Ikram ELMOUHIB**  
- **Soukaina EL HASOUBI**

---

## Technologies utilisées

- **MySQL Workbench** : modélisation MCD/MLD + génération des scripts SQL  
- **SQLite** : base de données légère embarquée  
- **Python 3** : développement de l’application  
- **Streamlit** : création rapide d’une interface web moderne  

---

## Structure du projet

PROJET-BD/
│
├── HotelManagement.sql  # Scripts de création des tables et les requêtes SQL
│
├── HotelManagement.py  # Code source de l'application Streamlit
│
├── Systeme_Gestion_Hoteliere.pdf  # Document PDF pour les requêtes en algèbre relationnelle
│
└── README.md  # fichier de documentation


---

## Instructions d’installation et d’exécution

### 1. Cloner le projet

git clone https://github.com/votre-utilisateur/projet-gestion-hoteliere.git
cd projet-gestion-hoteliere

### 2. Installer les dépendances

Assurez-vous d’avoir Python 3 installé, puis installez Streamlit :
pip install streamlit

### 3. Lancer l’application Streamlit

cd interface
streamlit run HotelManagement.py

### 4. Base de données

   * Par défaut, l’application utilise SQLite.
   * Pour tester avec MySQL, exécutez les scripts dans le dossier script_sql/ via MySQL Workbench.

## 📽️ Démonstration vidéo
 Cliquez ici pour voir la vidéo de démonstration
👉 https://drive.google.com/drive/folders/1WZZG6t2kszJGJSk7uSboSzfWaBSlSMhh

## Concepts abordés
   * Modélisation Entité-Association (MCD)
   * Transformation en MLD (Modèle Logique des Données)
   * Script SQL : CREATE, INSERT, SELECT, JOIN
   * Requêtes avancées : filtrage, agrégation, sous-requêtes
   * Connexion Python ↔ SQLite
   * Interface Streamlit interactive


## Encadré par
Pr. J. ZAHIR
Faculté des Sciences Semlalia – UCA

## Remarques finales
Ce projet nous a permis de consolider nos compétences en bases de données relationnelles et en développement d’interfaces web avec Python.
Nous remercions notre enseignant pour son accompagnement et ses conseils tout au long du module.