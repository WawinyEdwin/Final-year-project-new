import pandas as pd

#reading datasets
crop_data_path = 'Data-raw/cpdata.csv'
fertilizer_data_path = 'Data-raw/Fertilizer.csv'

crop = pd.read_csv(crop_data_path)
fert = pd.read_csv(fertilizer_data_path)

# Function for lowering the cases
def change_case(i):
    i = i.replace(" ", "")
    i = i.lower()
    return i

fert['Crop'] = fert['Crop'].apply(change_case)
crop['label'] = crop['label'].apply(change_case)

#feature transformation in ferttilizer dataset

fert['Crop'] = fert['Crop'].replace('mungbeans','mungbean')
fert['Crop'] = fert['Crop'].replace('lentils(masoordal)','lentil')
fert['Crop'] = fert['Crop'].replace('pigeonpeas(toordal)','pigeonpeas')
fert['Crop'] = fert['Crop'].replace('mothbean(matki)','mothbeans')
fert['Crop'] = fert['Crop'].replace('chickpeas(channa)','chickpea')

del fert['Unnamed: 0']

crop_names = crop['label'].unique()
crop_names_from_fert = fert['Crop'].unique()
extract_labels = []
for i in crop_names_from_fert:
    if i in crop_names:
        extract_labels.append(i)

# 1 Creating empty dataframe with crop columns and fertilizer columns
new_crop = pd.DataFrame(columns = crop.columns)
new_fert = pd.DataFrame(columns = fert.columns)

# using extract labels on crop to get all the data related to those labels
for label in extract_labels:
    new_crop = new_crop.append(crop[crop['label'] == label])
for label in extract_labels:
    new_fert = new_fert.append(fert[fert['Crop'] == label].iloc[0])
new_crop.to_csv('Data_raw/Prepared_Crop.csv')
new_fert.to_csv('Data_raw/Prepared_Fertilizer.csv')
print('success')