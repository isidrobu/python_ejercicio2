#!/usr/python
# -*- coding: utf-8 -*-

import MySQLdb


# Establecemos la conexión
Conexion = MySQLdb.connect(host='localhost', user='root',passwd='root', db='DBdeConan')


# Creamos el cursor
micursor = Conexion.cursor()


#creamos los 10 registro iniciales
micursor.execute("INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (1, \"Ejercito de Zombies\",\"Muertos Vivientes\",\"Desmembramiento a espada\");")
micursor.execute("INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (2, \"isidro\",\"estudiante\",\"accidente\");")
micursor.execute("INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (3, \"pepe\",\"comercial\",\"accidente\");")
micursor.execute("INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (4, \"juan\",\"camarero\",\"apuñalado\");")
micursor.execute("INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (5, \"maria\",\"cocinera\",\"accidente laboral\");")

Conexion.commit()
micursor.close () 
Conexion.close () 
