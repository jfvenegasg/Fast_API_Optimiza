from pyomo.environ import *
import pickle
import pandas as pd

modelo=ConcreteModel()

modelo.x1=Var(within=Binary,bounds=(0,1))
modelo.x2=Var(within=Binary,bounds=(0,1))
modelo.x3=Var(within=Binary,bounds=(0,1))
modelo.x4=Var(within=Binary,bounds=(0,1))
modelo.x5=Var(within=Binary,bounds=(0,1))

v1=0.2
v2=0.2
v3=0.2
v4=0.2
v5=0.2

w1=0
w2=0
w3=0
w4=0
w5=0

peso_total=0

objeto1_peso = float(input('Peso Objeto 1: '))
objeto2_peso = float(input('Peso Objeto 2: '))
objeto3_peso = float(input('Peso Objeto 3: '))
objeto4_peso = float(input('Peso Objeto 4: '))
objeto5_peso = float(input('Peso Objeto 5: '))
peso_total = float(input('Peso Total: '))


data = pd.DataFrame({'Peso Objeto 1': [objeto1_peso],'Peso Objeto 2': [objeto2_peso], 'Peso Objeto 3': [objeto3_peso], 
                         'Peso Objeto 4': [objeto4_peso],'Peso Objeto 5': [objeto5_peso],'Peso Total': [peso_total]})


modelo.objetivo = Objective(expr=v1*modelo.x1+v2*modelo.x2+v3*modelo.x3+v4*modelo.x4+v5*modelo.x5, sense=maximize)

modelo.restriccion = Constraint(expr=data.iloc[0,0]*modelo.x1 + data.iloc[0,1]*modelo.x2+data.iloc[0,2]*modelo.x3+
                                    data.iloc[0,3]*modelo.x4+data.iloc[0,4]*modelo.x5 <= data.iloc[0,5])

glpsol_path = 'app\glpk-4.65\w64\glpsol.exe'

solver = SolverFactory('glpk', executable=glpsol_path)  
solver.set_executable(executable='app/glpk-4.65/w64/glpsol.exe', validate=False)

resultado = solver.solve(modelo)
print(resultado)


#pickle.dump(modelo, open('app/modelo_optimizacion/modelo.pkl','wb'))


