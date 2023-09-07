import sys
from zipfile import ZipFile
import pandas as pd
import sqlite3
from os import remove

basededatos = 'coches.bd'

def precio_medio_por_marca(conexion):
	cursor = conexion.cursor()
	cursor.execute("SELECT marca, AVG(precio) FROM coches GROUP BY marca")
	datos = cursor.fetchall()
	return datos

def marca_coche_mas_barato(conexion):
	cursor = conexion.cursor()
	cursor.execute("SELECT marca,modelo, MIN (precio) FROM coches")
	datos = cursor.fetchall()
	return datos

def precio_total_coches(conexion):
	cursor = conexion.cursor()
	cursor.execute('SELECT SUM(precio) FROM coches')
	dato = cursor.fetchall()
	numero = dato[0] [0]
	return numero

def numero_coches_tabla(conexion):
	cursor = conexion.cursor()
	cursor.execute('SELECT COUNT (*) FROM coches')
	dato = cursor.fetchall()
	numero = dato[0] [0]
	return numero

def consultar_coches(conexion):
	cursor = conexion.cursor()
	cursor.execute('SELECT * FROM coches LIMIT 20')
	filas = cursor.fetchall()
	for fila in filas:
		print (fila)

def borrar_datos():
 	try:
 		remove (basededatos)
 	except FileNotFoundError:
 		pass

def insertar_tabla_coches(conexion,coche):
	cursor = conexion.cursor()
	cursor.execute('INSERT INTO coches (marca,modelo,combustible, transmision, estado, matriculacion, kilometraje,potencia,precio) VALUES (?,?,?,?,?,?,?,?,?)',coche)
	conexion.commit()

def grabar_coche(conexion,datos):
	for fila in datos.itertuples():
		marca = fila [1]
		modelo = fila [2]
		combustible = fila [3]
		transmision = fila [4]
		estado = fila [5]
		matriculacion = fila [6]
		kilometraje = fila [7]
		potencia = fila [8]
		precio = fila [9]

		coche = (marca,modelo,combustible, transmision, estado, matriculacion, kilometraje,potencia,precio)
		insertar_tabla_coches(conexion,coche)



		

def crear_tabla_coches(conexion):
	cursor = conexion.cursor()
	cursor.execute('CREATE TABLE coches(marca text, modelo text, combustible text, transmision text, estado text, matriculacion text, Kilometraje integer, potencia real, precio real)')
	conexion.commit()

def crear_conexion_bd():
	try:
		conexion = sqlite3.connect(basededatos)
		return conexion
	except Error:
		print (Error)

def leer_datos(nombre):
	datos = pd.read_csv(nombre, sep= ';')
	return datos

def descomprimir_fichero(nombre):
	with ZipFile (nombre, 'r') as zip:
		zip.extractall()

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print ("Numero de parametros incorrectos. Puede faltar el nombre del archivo");
	else:
		nombre_fichero = sys.argv[1]
		borrar_datos() 		
		descomprimir_fichero(nombre_fichero)
		datos = leer_datos(nombre_fichero)
		print (datos);
		conexion = crear_conexion_bd()
		crear_tabla_coches(conexion)
		grabar_coche(conexion,datos)
		print ('\n Consultamos los datos de la tabla')
		consultar_coches (conexion)
		dato = numero_coches_tabla(conexion)
		print('\n El numero de coches es de {}'.format(dato))
		numero = precio_total_coches(conexion)
		dinero = '{:,}'.format(numero).replace(',','.')
		print ("\n El precio total de los coches es de {}".format(dinero))
		datos = marca_coche_mas_barato(conexion)
		marca = datos [0] [0]
		modelo = datos [0] [1]
		precio = datos [0] [2]
		print ('\n coche mas barato. Marca = {}, modelo ={} precio = {}'.format(marca,modelo,precio));
		print ('\n Precio medio por marca \n');
		datos = precio_medio_por_marca(conexion)
		for dato in datos:
			marca = dato[0]
			precio = dato [1]
			print (marca,precio);



		

