import os
import pandas as pd
import numpy as np
from scipy.integrate import trapz

draw = "drawing_data.csv"

def test_data(df):
   
    pen_lifts = Lift(df)
    regularity_score = Smooth_scores(df)
    symmetry_score = symmetry_scores(df)

   
    for i in range(len(df)):
        x, y = df.iloc[i]['x'], df.iloc[i]['y']
        distance = np.sqrt(x**2 + y**2)

        df.at[i, 'distance'] = distance
        df.at[i, 'area'] = trapz(df['distance'].iloc[:i+1], dx=1)
        df.at[i, 'pen_lifts'] = pen_lifts
        df.at[i, 'regularity_score'] = regularity_score
        df.at[i, 'symmetry_score'] = symmetry_score

    return df

def Lift(df):
    df.reset_index(drop=True, inplace=True)
    pressure_threshold = 0
    df['pen_lifted'] = df['pressure'] == pressure_threshold

    pen_lifts = df['pen_lifted'].sum()

    return pen_lifts

def Smooth_scores(df):
    distances = np.sqrt((df['x'].diff() ** 2) + (df['y'].diff() ** 2))
    avg_distance = distances.mean()
    std_distance = distances.std()
    regularity_score = avg_distance / std_distance
    return regularity_score

def symmetry_scores(df):
    df = df.assign(theta=np.arctan2(df['y'], df['x']))
    x_mean = df['x'].mean()
    y_mean = df['y'].mean()
    df['dist'] = np.sqrt((df['x'] - x_mean) ** 2 + (df['y'] - y_mean) ** 2)

    quarter_turns = np.linspace(0, 1.5 * np.pi, num=7)
    quarter_distances = []
    for i in range(len(quarter_turns) - 1):
        start = quarter_turns[i]
        end = quarter_turns[i + 1]
        subset = df[(df['theta'] >= start) & (df['theta'] < end)]
        quarter_distances.append(subset['dist'].mean())

    symmetry_score = max(quarter_distances) / min(quarter_distances)
    return symmetry_score

data = pd.read_csv(draw)

def process(data):
    processed_data = test_data(data)


    processed_data.to_csv("processed_drawing_data.csv", index=False)

    return processed_data



