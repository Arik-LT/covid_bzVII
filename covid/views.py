from flask import render_template, request
from covid import app
import csv
import json
from datetime import date


@app.route("/provincias")
def provincias():
    fichero = open ("data/provincias.csv", "r", encoding = "utf8")
    csvreader = csv.reader(fichero, delimiter= ",")

    lista = []
    for registro in csvreader:
        lista.append({"codigo":registro[0], "valor":registro[1]})
    
    fichero.close()
    print(lista)
    return json.dumps(lista)

@app.route("/provincias/<codigo>")
def laprovincia(codigo):
    fichero = open ("data/provincias.csv", "r", encoding = "utf8")
    dictreader = csv.DictReader(fichero, fieldnames =["codigo", "provincia"])
    
    for registro in dictreader:
        if registro["codigo"] == codigo:
            return registro["provincia"]
        
    fichero.close()
    return "El codigo no existe"

@app.route("/casos/<int:year>", defaults={'mes': None, 'dia':None})
@app.route("/casos/<int:year>/<int:mes>")
@app.route("/casos/<int:year>/<int:mes>/<int:dia>")
def casos(year, mes, dia = None):

    if not mes:
        fecha = "{:04d}".format(year)
    elif not dia: 
        fecha = "{:04d}-{:02d}".format(year, mes)
    else: 
        fecha = "{:04d}-{:02d}-{:02d}".format(year, mes, dia)


    fichero = open ("data/casos_diagnostico_provincia.csv", "r", encoding = "utf8")
    dictReader = csv.DictReader(fichero)
    
    res = {"num_casos":0,
    "num_casos_prueba_pcr":0,
    "num_casos_prueba_test_ac":0,
    "num_casos_prueba_ag":0,
    "num_casos_prueba_elisa":0,
    "num_casos_prueba_desconocida":0
    }

    for registro in dictReader:
        if fecha in registro["fecha"]:
            for clave in res:
                res[clave] += int(registro[clave])

        elif registro["fecha"] > fecha:
            break

    fichero.close()
    return json.dumps(res)

@app.route("/incidenciadiaria", methods = ["GET", "POST"])
def incidencia():
    formulario = {
        'provincia': '',
        'fecha': str(date.today()),
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0, 
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0
    }

    fichero = open('data/provincias.csv', 'r')
    csvreader = csv.reader(fichero, delimiter=",")
    next(csvreader)
    lista = []
    for registro in csvreader:
        d = {'codigo': registro[0], 'descripcion': registro[1]}
        lista.append(d)

    fichero.close()
        
    if request.method == 'GET':
        return render_template("alta.html", datos=formulario, 
                            provincias=lista, error="")

    for clave in formulario:
        formulario[clave] = request.form[clave]

    #validar que num_casos en general es no negativo
    num_pcr = request.form['num_casos_prueba_pcr']
    try:
        num_pcr = int(num_pcr)
        if num_pcr < 0:
            raise ValueError('Debe ser no negativo')
    except ValueError:
        return render_template("alta.html", datos=formulario, error = "PCR no puede ser negativa")
        
    return 'Ha hecho un post'

@app.route("/jinjaestirao")
def j1():
    return render_template("prueba.txt", provincias=[{'codigo': 'M', 'descripcion': 'Madrid'},
                                                    {'codigo': 'CC', 'descripcion': 'Cáceres'}])