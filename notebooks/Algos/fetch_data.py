# Le fichier utilisé est celui de Sara-Hojjati : https://github.com/Sara-Hojjati/predicting_mortality_mimic
#assuming that we have already connected to the data base, we fetch this data:
#Hospital_Expire_Flag: Binary variable indicating whether the patient died (1) or survived (0)
#during the hospital stay.
#My predictors are:
#Gender: Categorical variable indicating the patient's gender.
#Age_at_Admission: Numerical variable representing the patient's age at the time of hospital admission.
#ICU_Length_of_Stay: Numerical variable indicating the length of the patient's stay in the ICU, in days.
#Admission_Type: Categorical variable indicating the type of admission (e.g., EMERGENCY, URGENT, ELECTIVE).
#%%
import numpy as np
import pandas as pd
import psycopg2
import subprocess
#%%
query = """
SELECT
    p.subject_id,
    p.gender,
    EXTRACT(epoch FROM (a.admittime - p.dob))/31557600 AS age_at_admission,
    a.hospital_expire_flag,
    icu.los AS icu_length_of_stay,
    a.admission_type,
    COUNT(DISTINCT diag.icd9_code) AS num_diagnoses,
    COUNT(DISTINCT proc.icd9_code) AS num_procedures,
    AVG(chart.hr) AS avg_heart_rate,
    AVG(chart.bp) AS avg_blood_pressure,
    AVG(lab.hemoglobin) AS avg_hemoglobin,
    AVG(lab.sodium) AS avg_sodium,
    AVG(lab.potassium) AS avg_potassium,
    AVG(meds.dose_val_rx) AS avg_med_dose
FROM mimiciii.patients p
INNER JOIN mimiciii.admissions a ON p.subject_id = a.subject_id
INNER JOIN mimiciii.icustays icu ON a.hadm_id = icu.hadm_id
LEFT JOIN mimiciii.diagnoses_icd diag ON a.hadm_id = diag.hadm_id
LEFT JOIN mimiciii.procedures_icd proc ON a.hadm_id = proc.hadm_id
LEFT JOIN (
    SELECT subject_id, hadm_id, icustay_id,
           AVG(CASE WHEN itemid IN (211,220045) THEN valuenum ELSE NULL END) AS hr,
           AVG(CASE WHEN itemid IN (220050,220051) THEN valuenum ELSE NULL END) AS bp
    FROM mimiciii.chartevents
    WHERE itemid IN (211,220045,220050,220051)
    AND valuenum IS NOT NULL
    GROUP BY subject_id, hadm_id, icustay_id
) chart ON icu.icustay_id = chart.icustay_id
LEFT JOIN (
    SELECT subject_id, hadm_id,
           AVG(CASE WHEN itemid = 50811 THEN valuenum ELSE NULL END) AS hemoglobin,
           AVG(CASE WHEN itemid = 50824 THEN valuenum ELSE NULL END) AS sodium,
           AVG(CASE WHEN itemid = 50822 THEN valuenum ELSE NULL END) AS potassium
    FROM mimiciii.labevents
    WHERE itemid IN (50811, 50824, 50822)
    AND valuenum IS NOT NULL
    GROUP BY subject_id, hadm_id
) lab ON a.hadm_id = lab.hadm_id
LEFT JOIN (
    SELECT subject_id, hadm_id, AVG(CAST(dose_val_rx AS NUMERIC)) AS dose_val_rx
    FROM mimiciii.prescriptions
    WHERE dose_val_rx IS NOT NULL AND dose_val_rx ~ '^[0-9.]+$'
    GROUP BY subject_id, hadm_id
) meds ON a.hadm_id = meds.hadm_id
WHERE a.hospital_expire_flag IS NOT NULL
AND EXTRACT(epoch FROM (a.admittime - p.dob))/31557600 > 18
GROUP BY p.subject_id, p.gender, a.hospital_expire_flag, icu.los, a.admission_type, EXTRACT(epoch FROM (a.admittime - p.dob))/31557600, icu.icustay_id;

"""

#%%
cur.execute(query)
data = cur.fetchall()
#%%
# Define the column names for your DataFrame
column_names = [
    "Subject_ID", "Gender", "Age_at_Admission", "Hospital_Expire_Flag",
    "ICU_Length_of_Stay", "Admission_Type", "Num_Diagnoses", "Num_Procedures",
    "Avg_Heart_Rate", "Avg_Blood_Pressure", "Avg_Hemoglobin",
    "Avg_Sodium", "Avg_Potassium", "Avg_Med_Dose"
]

# Create a pandas DataFrame with the fetched data
df = pd.DataFrame(data, columns=column_names)
#%%
# uncomment if you want to drop rows with missing values
#df=df.dropna()
#%%
df.to_csv('C:/Users/raw_data.csv',index=False)
