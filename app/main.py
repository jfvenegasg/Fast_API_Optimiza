import pandas as pd
from fastapi import FastAPI
import numpy as np
from pydantic import BaseModel
import pickle
from pyomo.environ import *

app = FastAPI()
modelo = pickle.load(open("app/modelo_optimizacion/modelo.pkl", "rb"))


class Model(BaseModel):
    objeto1_peso: float
    objeto2_peso: float
    objeto3_peso: float
    objeto4_peso: float
    objeto5_peso: float
    peso_total: float

@app.get("/")
def main():
    return "Bienvenido a FastAPI Optimiza"

# Parametros
@app.get("/Optimizacion Combinatoria")
def model_1(objeto1_peso:float,objeto2_peso:float,objeto3_peso:float,objeto4_peso:float,objeto5_peso:float,peso_total:float):
    # Se importa el modelo de regresion
    data = pd.DataFrame({'Peso Objeto 1': [objeto1_peso],'Peso Objeto 2': [objeto2_peso], 'Peso Objeto 3': [objeto3_peso], 
                         'Peso Objeto 4': [objeto4_peso],'Peso Objeto 5': [objeto5_peso],'Peso Total': [peso_total]})

    modelo.restriccion = Constraint(expr=data.iloc[0,0]*modelo.x1 + data.iloc[0,1]*modelo.x2+data.iloc[0,2]*modelo.x3+
                                    data.iloc[0,3]*modelo.x4+data.iloc[0,4]*modelo.x5 <= data.iloc[0,5])


    glpsol_path = 'app/glpk-4.65/w64/glpsol.exe'
    #solver.set_executable(executable='app/glpk-4.65/w64/glpsol.exe', validate=False)
    solver = SolverFactory('glpk', executable=glpsol_path)  

    resultado = solver.solve(modelo)

       
    return {"El peso de la mochila es de:":value(modelo.x1)*data.iloc[0,0]+value(modelo.x2)*data.iloc[0,1]+value(modelo.x3)*data.iloc[0,2]+
            value(modelo.x4)*data.iloc[0,3]+value(modelo.x5)*data.iloc[0,4],
             "x1 =": value(modelo.x1),"x2 =": value(modelo.x2),"x3 =": value(modelo.x3),"x4 =": value(modelo.x4),"x5 =": value(modelo.x5)}

