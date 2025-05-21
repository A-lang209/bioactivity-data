#Install the ChEMBL web service package so that we can retrieve bioactivity data from the ChEMBL Database.
! pip install chembl_webresource_client

## **Importing libraries**

# Import necessary libraries
import pandas as pd
from chembl_webresource_client.new_client import new_client

#Target search for coronavirus
# Target search for coronavirus
target = new_client.target
target_query = target.search('coronavirus')
targets = pd.DataFrame.from_dict(target_query)
targets


### **Select and retrieve bioactivity data for *SARS coronavirus 3C-like proteinase* (seventh entry)**
selected_target = targets.target_chembl_id[6]
selected_target

activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")

df = pd.DataFrame.from_dict(res)
df.head(3)

df.standard_type.unique()

#Finally we will save the resulting bioactivity data to a CSV file **bioactivity_data.csv**.
df.to_csv('bioactivity_data.csv', index=False)

## **Copying files to Google Drive**
from google.colab import drive
drive.mount('/content/gdrive/', force_remount=True)

#Next, we create a **data** folder in our **Colab Notebooks** folder on Google Drive.
! mkdir "/content/gdrive/My Drive/Colab Notebooks/data2"
! cp bioactivity_data.csv "/content/gdrive/My Drive/Colab Notebooks/data"
! ls -l "/content/gdrive/My Drive/Colab Notebooks/data"

#Let's see the CSV files that we have so far.
bioactivity_data.csv  gdrive  sample_data

#Taking a glimpse of the **bioactivity_data.csv** file that we've just created.
! head bioactivity_data.csv

### **Handling missing data**
df2 = df[df.standard_value.notna()]
df2

### **Labeling compounds as either being active, inactive or intermediate**
bioactivity_class = []
for i in df2.standard_value:
  if float(i) >= 10000:
    bioactivity_class.append("inactive")
  elif float(i) <= 1000:
    bioactivity_class.append("active")
  else:
    bioactivity_class.append("intermediate")

#### **Iterate the *molecule_chembl_id* to a list**
mol_cid = []
for i in df2.molecule_chembl_id:
  mol_cid.append(i)

#### **Iterate *canonical_smiles* to a list**
canonical_smiles = []
for i in df2.canonical_smiles:
  canonical_smiles.append(i)
  
### **Iterate *standard_value* to a list**
standard_value = []
for i in df2.standard_value:
  standard_value.append(i)

#Alternative method
selection = ['molecule_chembl_id', 'canonical_smiles', 'standard_value']
df3 = df2[selection]
df3

### **Combine the 4 lists into a dataframe**
data_tuples = list(zip(mol_cid, canonical_smiles, bioactivity_class, standard_value))
df3 = pd.DataFrame( data_tuples,  columns=['molecule_chembl_id', 'canonical_smiles', 'bioactivity_class', 'standard_value'])
df3

### **Alternative method**
selection = ['molecule_chembl_id', 'canonical_smiles', 'standard_value']
df3 = df2[selection]
df3

pd.concat([df3,pd.Series(bioactivity_class)], axis=1)

#Saves dataframe to CSV file
df3.to_csv('bioactivity_preprocessed_data.csv', index=False)
! cp bioactivity_preprocessed_data.csv "/content/gdrive/My Drive/Colab Notebooks/data"
! ls "/content/gdrive/My Drive/Colab Notebooks/data"











