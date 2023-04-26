import os
import pandas as pd
import numpy as np
from scipy.integrate import trapz

# Paths
parkinson = '../Parkinsons_Data/PARKINSON_HW/hw_dataset/parkinson/'
control = '../Parkinsons_Data/PARKINSON_HW/hw_dataset/control/'
test_dir = "../Parkinsons_Data/PARKINSON_HW/new_dataset/parkinson/"


def combined():
    df_list = []
    combined_data =pd.DataFrame()

    for filename in os.listdir(control):
        if filename.endswith('.txt'):
        
            df = pd.read_csv(os.path.join(control, filename), delimiter=';', names=['X', 'Y', 'Z', 'Pressure', 'GripAngle', 'Timestamp', 'TestID'])
       
            df_list.append(df)
            df["Parkinson"] = 0

    Control_result = pd.concat(df_list, ignore_index=True)
    df_list = []


    for filename in os.listdir(parkinson):
        if filename.endswith('.txt'):
        
            df = pd.read_csv(os.path.join(parkinson, filename), delimiter=';', names=['X', 'Y', 'Z', 'Pressure', 'GripAngle', 'Timestamp', 'TestID'])
       
            df_list.append(df)
            df["Parkinson"] = 1

    Parkinson_result = pd.concat(df_list, ignore_index=True)
    combined_data = pd.concat([Parkinson_result, Control_result], ignore_index=True)

    return combined_data

# Process directories
def process_directory(txt_dir, parkinson_value):
    dataframes = []
    
    for filename in os.listdir(txt_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(txt_dir, filename)
            df = pd.read_csv(filepath, delimiter=';', names=['X', 'Y', 'Z', 'Pressure', 'GripAngle', 'Timestamp'])
            df['Parkinsons'] = parkinson_value
            
            dataframes.append(df)
    
    return dataframes


parkinson_dataframes = process_directory(parkinson, 1)
control_dataframes = process_directory(control, 0)
test_dataframes = process_directory(test_dir, 1)




# Pre-Processing Features for training


def aggregate_data(control_dir, parkinson_dir):
    agg_data = pd.DataFrame()

  
    for filename in os.listdir(control_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(control_dir, filename)
            df = pd.read_csv(filepath, delimiter=';', names=['X', 'Y', 'Z', 'Pressure', 'GripAngle','Timestamp'])
            distances = []
            for i in range(len(df)):
                x, y = df.iloc[i]['X'], df.iloc[i]['Y']
                distance = np.sqrt(x**2 + y**2)
                distances.append(distance)

            
            area = trapz(distances, dx=1)

            df['area'] = area
            df = pd.DataFrame(df.mean(skipna=True, numeric_only=True)).T
            df['Parkinsons'] = 0 s
            agg_data = pd.concat([agg_data, df], ignore_index=True)

    for filename in os.listdir(parkinson_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(parkinson_dir, filename)
            df = pd.read_csv(filepath, delimiter=';', names=['X', 'Y', 'Z', 'Pressure', 'GripAngle','Timestamp'])
            distances = []
            for i in range(len(df)):
                x, y = df.iloc[i]['X'], df.iloc[i]['Y']
                distance = np.sqrt(x**2 + y**2)
                distances.append(distance)

  
            area = trapz(distances, dx=1)
            df['area'] = area
            df = pd.DataFrame(df.mean(skipna=True, numeric_only=True)).T
            df['Parkinsons'] = 1  
            agg_data = pd.concat([agg_data, df], ignore_index=True)
    
    return agg_data



def test_data(test_dir):
    agg_data = pd.DataFrame()
    for filename in os.listdir(test_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(test_dir, filename)
            df = pd.read_csv(filepath, delimiter=';', names=['X', 'Y', 'Z', 'Pressure', 'GripAngle','Timestamp'])
            distances = []
            for i in range(len(df)):
                x, y = df.iloc[i]['X'], df.iloc[i]['Y']
                distance = np.sqrt(x**2 + y**2)
                distances.append(distance)

            
            area = trapz(distances, dx=1)
            df['area'] = area
            df = pd.DataFrame(df.mean(skipna=True, numeric_only=True)).T
            df['Parkinsons'] = 1  
            agg_data = pd.concat([agg_data, df], ignore_index=True)
    return agg_data


def Lift(txt_dir):
    total_pen_lifts = 0
    list_lift = []
    for filename in os.listdir(txt_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(txt_dir, filename)
            df = pd.read_csv(filepath, delimiter=';', names=['X', 'Y', 'Z', 'Pressure', 'GripAngle', 'Timestamp', 'TestID'])
            df.reset_index(drop=True, inplace=True)  # Reset the index
            pressure_threshold = 0
            df['pen_lifted'] = df['Pressure'] <= pressure_threshold

            pen_lifts = 0
            for i in range(1, len(df)):
                if df.loc[i, 'pen_lifted'] and not df.loc[i - 1, 'pen_lifted']:
                    pen_lifts += 1
            total_pen_lifts += pen_lifts
            list_lift.append(pen_lifts)

    return list_lift







# Smooth
def Smooth_scores(txt_dir):
    regularity_scores = []
    for filename in os.listdir(txt_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(txt_dir, filename)
            df = pd.read_csv(filepath, delimiter=';', names=['X', 'Y', 'Z', 'Pressure', 'GripAngle', 'Timestamp'])


            distances = np.sqrt((df['X'].diff() ** 2) + (df['Y'].diff() ** 2))

            avg_distance = distances.mean()
            std_distance = distances.std()
            regularity_score = avg_distance / std_distance
            regularity_scores.append(regularity_score)

    return regularity_scores



# Symmetry 
def symmetry_scores(txt_dir):
    avg_sym = []
    for filename in os.listdir(txt_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(txt_dir, filename)
            df = pd.read_csv(filepath, delimiter=';',  names=['X', 'Y', 'Z', 'Pressure', 'GripAngle', 'Timestamp'])


            df = df.assign(theta=np.arctan2(df['Y'], df['X']))
         
            x_mean = df['X'].mean()
            y_mean = df['Y'].mean()
            df['dist'] = np.sqrt((df['X'] - x_mean) ** 2 + (df['Y'] - y_mean) ** 2)

           
            quarter_turns = np.linspace(0, 1.5 * np.pi, num=7)
            quarter_distances = []
            for i in range(len(quarter_turns) - 1):
                start = quarter_turns[i]
                end = quarter_turns[i+1]
                subset = df[(df['theta'] >= start) & (df['theta'] < end)]
                quarter_distances.append(subset['dist'].mean())

           
            symmetry_score = max(quarter_distances) / min(quarter_distances)
            avg_sym.append(symmetry_score)
    
    return avg_sym


def Time(txt_dir):
    total_times = []
    for filename in os.listdir(txt_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(txt_dir, filename)
            df = pd.read_csv(filepath, delimiter=';',  names=['X', 'Y', 'Z', 'Pressure', 'GripAngle', 'Timestamp'])

            start_time = df['Timestamp'].min()
            end_time = df['Timestamp'].max()
            total_time = end_time - start_time
            total_times.append(total_time)
    return total_times
