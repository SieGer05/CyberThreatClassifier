# NetAttackML

## **Description**

This project models attacker behavior in network traffic using Machine Learning techniques.  
It begins with **binary classification** (attack vs. normal traffic), and will later expand to multi-class classification to detect specific types of attacks (DoS, DDoS, Web attacks, etc.).

> **Note:** This project, including code and documentation, is written in **French**.

---

## **Objectif**

Développer un modèle intelligent capable de détecter les comportements malveillants à partir du trafic réseau, à l’aide de techniques de Machine Learning.  

À ce stade du projet, un modèle de **classification binaire** a été entraîné pour distinguer les attaques du trafic légitime.

---

## **Fichier principal**

- `NetAttackML.ipynb` : Notebook contenant les étapes de traitement des données, d'entraînement du modèle binaire, et d’évaluation initiale.

---

## **Interface Graphique (GUI)**

Nous avons ajouté une interface utilisateur interactive avec **Streamlit** pour faciliter la démonstration du modèle.  

### Comment exécuter l'interface :

1. Installer les dépendances via :  
```bash
pip install -r requirements.txt
```

2. Lancer l’application Streamlit :

```bash
streamlit run streamlit-attack-detector/app.py
```

- **Fonctionnalités de l’application :**

- **Objectif :**
Simuler un administrateur réseau qui utilise cet outil pour analyser un échantillon de trafic réseau (ex. : un fichier CSV capturé), et déterminer si une attaque est en cours.

- **Rôle utilisateur :**
Un analyste SOC ou un administrateur réseau, qui souhaite vérifier si un extrait du trafic contient une attaque.

- **Entrée :**
Un fichier .csv contenant quelques connexions réseau capturées avec les 70 features du dataset. Exemple : sample_traffic.csv

- **Étapes de la démonstration :**

L’utilisateur charge le fichier dans l’interface (via drag & drop ou bouton).

- **Le modèle applique successivement :**

	- StandardScaler pour normaliser les données,
	- PCA pour réduction de dimension,
	- Le modèle SVM avec noyau RBF pour la prédiction.

- **Affichage final dans l’interface :**

ID	Résultat	Probabilité attaque
1      Benign	     0.03
2	    Malicious	 0.92

- **Phrase de conclusion affichée à l’utilisateur :**
*"En quelques secondes, notre modèle identifie automatiquement les comportements anormaux dans le trafic réseau. Cela permet aux analystes de réagir plus vite face aux attaques en cours."*

- **Génération d’un fichier test aléatoire**
Un script est également fourni pour générer un fichier .csv ou .xlsx de test contenant 100 lignes sélectionnées aléatoirement à partir de plusieurs fichiers de données brutes.
Ce fichier est utile pour tester rapidement l’application sans manipuler les gros datasets originaux.

**Pour exécuter ce script :**

```Bash
python generate_random_sample.py
```

---

## **Dataset**

Le dataset utilisé est disponible sur Kaggle :
[CICIDS2017 - Intrusion Detection Evaluation Dataset](https://www.kaggle.com/datasets/dhoogla/cicids2017)

---
## **Auteurs**

- JAOUAD Salah-Eddine
- DJILI Mohamed Amine

Étudiants ingénieurs en 4ᵉ année, spécialité Cybersécurité et Confiance Numérique,
*ENSET Mohammedia – Université Hassan II de Casablanca*.

---
## **Prochaines étapes**

- Étendre le modèle vers une classification multi-classes pour identifier différents types d’attaques réseau.

- Intégrer ce modèle multi-classes dans l’interface graphique existante.

- Ajouter des visualisations et une évaluation plus approfondie.

---
## **Statut du projet**

🚧 En cours – Étape actuelle : classification binaire (attaque vs normal) avec interface Streamlit fonctionnelle.