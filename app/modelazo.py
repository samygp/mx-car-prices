from pandas import DataFrame
from sklearn import linear_model
from joblib import load
from json import loads
from datetime import datetime as dt

class ModeloCarros():
    def __init__(self, modelo='modelazo.joblib', columnas='columnas.json'):
        with open(columnas) as col_file:
            self.X_template = loads(col_file.read())
        self.modelo = load(modelo)

    def get_row(self, marca_modelo, anio, km):
        curr_year = dt.now().year
        y_old = curr_year - anio
        self.X_template['km'] = [km]
        self.X_template['y_old'] = [y_old]
        self.X_template[marca_modelo] = [1]
        # Crear DataFrame con una fila
        df = DataFrame(self.X_template)
        # "Resetear" el modelo de coche usado
        self.X_template[marca_modelo] = [0]
        return df

    def predecir(self, marca_modelo, anio, km):
        row = self.get_row(marca_modelo, anio, km)
        print(row)
        result = int(self.modelo.predict(row)[0])
        if result < 0:
            return f"El resultado encontrado ({result}) no tiene mucho sentido, probablemente no había suficiente información de entrenamiento para los valores solicitados. Prueba con un modelo de anio mas reciente"
        return result

"""
m = modelazo.ModeloCarros()
km = 67445
anio = 2015
marca_modelo = "chevrolet_aveo"
m.predecir(marca_modelo, anio, km)
# 110996
"""