import pandas as pd

#Read DataSets
fertilizer_data_path = 'Data-raw/FertilizerData.csv'
merge_fert = pd.read_csv(fertilizer_data_path)

del merge_fert['Unnamed: 0.1']
del merge_fert['Unnamed: 0']

merge_crop = pd.read_csv('Data-raw/MergeFileCrop.csv')
reco_fert = merge_fert

#Add +/-3 for every NPK value
import random
temp = pd.DataFrame(columns = ['N','P','K'])
for i in range(0,merge_crop.shape[0]):
    crop = merge_crop.label.iloc[i]
    #print(crop)
    N = reco_fert[reco_fert['Crop'] == crop]["N"].iloc[0] + random.randint(-20,20)
    P = reco_fert[reco_fert['Crop'] == crop]["P"].iloc[0] + random.randint(-5,20)
    K = reco_fert[reco_fert['Crop'] == crop]["K"].iloc[0] + random.randint(-5,5)
    d = {"N":N,"P":P,"K":K}
    #print(d)
    temp = temp.append(d,ignore_index = True)

merge_crop['N'] = temp['N']
merge_crop['P'] = temp['P']
merge_crop['K'] = temp['K']

del merge_crop['Unnamed: 0']



merge_crop = merge_crop[[ 'N', 'P', 'K','temperature', 'humidity', 'ph', 'rainfall', 'label']]
merge_crop.to_csv("Prepared_data/crop_recommendation.csv",index=False)
