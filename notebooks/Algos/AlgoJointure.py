import pandas as pd

# Charger les données depuis les fichiers CSV
admission_df = pd.read_csv(r"C:\Users\idris\Downloads\Mimic\ADMISSIONS.csv")
patients_df = pd.read_csv(r"C:\Users\idris\Downloads\Mimic\PATIENTS.csv")

# Effectuer la jointure sur la colonne "SUBJECT_ID"
result_df = pd.merge(admission_df, patients_df, on="SUBJECT_ID")

# Afficher le résultat
print(result_df)
