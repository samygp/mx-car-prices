import pandas as pd
import numpy as np
from scipy.optimize import nnls
from sklearn import linear_model
from sklearn.model_selection import train_test_split

df_original = pd.read_csv("../data/carros_preprocessed.csv", index_col=0).reset_index(drop=True)

best_fit = 0

def obtener_training_set(df, lower_limit):
    counts = df.brand_model.value_counts()
    eliminar_modelos = [k for k,v in counts.items() if v < lower_limit]
    filtered_df = df[~df.brand_model.isin(eliminar_modelos)]
    #Obtener dummy variables
    dummies_df = pd.get_dummies(filtered_df['brand_model'])
    num_cols = ['y_old', 'km', 'price']
    return pd.concat([dummies_df, filtered_df[num_cols]], axis=1)

def entrenar(df, lower_limit):
    training_df = obtener_training_set(df, lower_limit)
    X = training_df.drop(['price'], axis=1)
    Y = training_df.price
    #Separar sets de entrenamiento y prueba
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = .10, random_state = 40)
    regr = linear_model.LinearRegression()
    regr.fit(X_train, Y_train)
    return regr.score(X_test, Y_test), training_df.shape[0]
    
score_best_fit = 0

results = []

for i in range(0, 400, 10):
    score, size = entrenar(df_original, i)
    results.append((i, score, size))
    if score > score_best_fit:
        score_best_fit = score
        best_fit = i

for r in results:
    print(r)
print("Best fit:", best_fit, "Score best fit:", score_best_fit)