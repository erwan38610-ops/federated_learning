# Le fichier utilisé est celui de Sara-Hojjati : https://github.com/Sara-Hojjati/predicting_mortality_mimic

# # Preprocess the raw data

#**Description:** This script is used to preprocess the raw data from MIMIC-III database that was saved in a csv file before.
# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.impute import KNNImputer
import seaborn as sns
import tensorflow as tf
# %%
# Load the raw data
df=pd.read_csv('C:/Users/sarho66/OneDrive - Linköpings universitet/mimic-iii/data/raw_data.csv')

# %%
# Make the categorical variables to be of type category
df['Hospital_Expire_Flag']=df['Hospital_Expire_Flag'].astype('category')
df['Gender']=df['Gender'].astype('category')
df['Admission_Type']=df['Admission_Type'].astype('category')
#%%
#Drop the columns with too many missing values
df.drop(['Subject_ID','Avg_Blood_Pressure','Avg_Hemoglobin','Avg_Sodium','Avg_Potassium'],axis=1,inplace=True)

#%%[markdown]
# ## Handling outliers
# %%[markdown]
#In the MIMIC-III (Medical Information Mart for Intensive Care III) database, patients with an age listed as 300 years are not actually 300 years old. This value is used to denote patients who are aged 89 years or older.
#%%
#turn the age to 90 if it is above 89
df['Age_at_Admission'] = df['Age_at_Admission'].apply(lambda x: 90 if x > 89 else x)
# %%
df[df['Avg_Heart_Rate']>220] #This cant happen so we will remove these values as they are probably due to entry errors
df.loc[df['Avg_Heart_Rate']>220,'Avg_Heart_Rate'] = np.nan

#%%[markdown]
# ## Normalizing the continuous variables
#%%
# Make all continues variables have the same scale from 0 to 1
df['ICU_Length_of_Stay'] = (df['ICU_Length_of_Stay'] - df['ICU_Length_of_Stay'].min()) / (df['ICU_Length_of_Stay'].max() - df['ICU_Length_of_Stay'].min())
df['Age_at_Admission'] = (df['Age_at_Admission'] - df['Age_at_Admission'].min()) / (df['Age_at_Admission'].max() - df['Age_at_Admission'].min())
df['Avg_Heart_Rate'] = (df['Avg_Heart_Rate'] - df['Avg_Heart_Rate'].min()) / (df['Avg_Heart_Rate'].max() - df['Avg_Heart_Rate'].min())
df['Avg_Med_Dose'] = (df['Avg_Med_Dose'] - df['Avg_Med_Dose'].min()) / (df['Avg_Med_Dose'].max() - df['Avg_Med_Dose'].min())
df['Num_Diagnoses'] = (df['Num_Diagnoses'] - df['Num_Diagnoses'].min()) / (df['Num_Diagnoses'].max() - df['Num_Diagnoses'].min())
df['Num_Procedures'] = (df['Num_Procedures'] - df['Num_Procedures'].min()) / (df['Num_Procedures'].max() - df['Num_Procedures'].min())
#%%
#Hot encoding
df = pd.get_dummies(df, columns=['Gender', 'Admission_Type'], drop_first=True).astype('float64')
#%%[markdown]
# # Handling missing values
#%%
# Perform KNN imputation for the entire training set and use it to transform the entire dataset
# we need to make sure that we fit the imputer only on the training set and not the entire dataset
#So first we will split the data into training and testing set
from sklearn.model_selection import train_test_split
#Defining X (features) and y (target)
X = df.drop(['Hospital_Expire_Flag'], axis=1)
y = df['Hospital_Expire_Flag'].astype('int64')
X.info()
y.info()
# %%
#Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
#%%
# Fitting the imputer on the training set and transforming the data
imputer = KNNImputer(n_neighbors=5, weights='uniform')
X_train_imputed_np = imputer.fit_transform(X_train)

# Converting the imputed data back to a DataFrame
X_train_imputed = pd.DataFrame(X_train_imputed_np, columns=X_train.columns, index=X_train.index)

#%%
# Transforming the test dataset
X_test_imputed_np = imputer.transform(X_test)

# Converting the imputed data back to a DataFrame, preserving the original index and column names
X_test_imputed = pd.DataFrame(X_test_imputed_np, columns=X_test.columns, index=X_test.index)

# %%
# %%
#%%
#Save the preprocessed data
#X_train_imputed.to_csv('C:/Users/sarho66/OneDrive - Linköpings universitet/mimic-iii/data/X_train_imputed.csv',index=False)
#X_test_imputed.to_csv('C:/Users/sarho66/OneDrive - Linköpings universitet/mimic-iii/data/X_test_imputed.csv',index=False)
#y_train.to_csv('C:/Users/sarho66/OneDrive - Linköpings universitet/mimic-iii/data/y_train.csv',index=False)
#y_test.to_csv('C:/Users/sarho66/OneDrive - Linköpings universitet/mimic-iii/data/y_test.csv',index=False)
# %%
df['Subject_ID'].nunique()

# %%
