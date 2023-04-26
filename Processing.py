import os
import pandas as pd
import numpy as np
from scipy.integrate import trapz

draw = "drawing_data.csv"

def test_data(df):
    distances = []
    for i in range(len(df)):
        x, y = df.iloc[i]['x'], df.iloc[i]['y']
        distance = np.sqrt(x**2 + y**2)
        distances.append(distance)

    area = trapz(distances, dx=1)
    df['area'] = area
    agg_data = pd.DataFrame(df.mean(skipna=True, numeric_only=True)).T
    return agg_data

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




