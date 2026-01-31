# federated_learning
Protection de la vie privée dans les bases de données de santé : enjeux et défis de l'apprentissage automatique



S - Situation

Dans le cadre d'un projet de groupe durant ma formation d'ingénieur, j'ai travaillé sur la base de données médicale MIMIC-III (MIT) contenant des données anonymisées de plus de 60 000 séjours en soins intensifs. L'enjeu était de traiter des données sensibles soumises au RGPD et au secret médical.



T - Tâche

Développer un modèle prédictif de décès des patients (Hospital_Expire_Flag).

Utiliser l'Apprentissage Fédéré (Federated Learning) pour éviter la centralisation des données.

Tester la robustesse du système face à deux attaques : l'inférence de source (SIA) et la suppression de gradients.



A - Action

Prétraitement : Nettoyage des données (6 329 patients), imputation par KNN pour les valeurs manquantes et équilibrage des classes avec SMOTE.

Modélisation : Implémentation d'un modèle Keras séquentiel intégré dans un processus de moyenne fédérée (FedAvg) via TensorFlow Federated.

Attaques : Simulation d'attaques bayésiennes pour identifier la provenance des données (SIA) et manipulation des poids du modèle pour isoler un client cible.



R - Résultat

Performance : Le modèle global a atteint une AUC de 0,96 et une précision de 0,88.

Sécurité : L'attaque SIA a démontré une précision de 78,27% pour identifier la source des données sur 2 clients, prouvant qu'un modèle performant reste vulnérable.

Recommandations : Proposition de contre-mesures comme l'ajout de bruit gaussien (confidentialité différentielle) et l'utilisation de fonctions LeakyReLU pour contrer la suppression de gradient.



Technologies Utilisées

Langage : Python (Pandas, NumPy, Scikit-Learn) 
Deep Learning : TensorFlow / Keras, TensorFlow Federated 


Statistiques : Tests de corrélation, imputation KNN
