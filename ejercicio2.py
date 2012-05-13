#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import pygtk
import gtk
import gtk.glade
import re


# Establecemos la conexión
Conexion = MySQLdb.connect(host='localhost', user='root',passwd='root', db='DBdeConan')


# Creamos el cursor
cursor = Conexion.cursor()


class Ejercicio2:
	def __init__(self):
		
		#Configuramos las variables para nuestra ventana-------
		self.wTree 	= gtk.glade.XML("ejercicio2.glade")
		#------------------------------------------------------
		
		#Configuramos los eventos mediante un diccionario de señales--
		dict = {"on_window1_delete_event":self.cerrar,
				"on_contactos_cursor_changed":self.copiaContactos,
				"on_agregar_clicked":self.agregar,
				"on_todos_clicked":self.todos2,
				"on_atras_clicked":self.todos3,
				"on_siguiente_clicked":self.todos4,
				"on_modificar_clicked":self.modificar,
				"on_borrar_clicked":self.borrar}
		self.wTree.signal_autoconnect(dict)		
		#------------------------------------------------------
		
		#Configuramos las variables de widget------------------
		self.id 		= self.wTree.get_widget("id")
		self.nombre 	= self.wTree.get_widget("nombre")
		self.profesion 	= self.wTree.get_widget("profesion")
		self.muerte 	= self.wTree.get_widget("muerte")
		self.contactos 	= self.wTree.get_widget("contactos")
		self.label		= self.wTree.get_widget("label")
		self.nombre.grab_focus()
		self.tree()
		self.blanco()
		self.todos(1)
		#------------------------------------------------------

	#Creamos la columna para contactos ---------------------
	def tree(self):
		self.llenatree("Id",0)
		self.llenatree("Nombre",1)
		self.llenatree("Profesion",2)
		self.llenatree("Muerte",3)
		self.lista = gtk.ListStore(int, str, str, str)
		self.contactos.set_model(self.lista)		
	#-------------------------------------------------------
	
	#Método para llenar el treeview con sus respectivas columnas -------------------
	def llenatree(self, titulo, columnId):
		column = gtk.TreeViewColumn(titulo, gtk.CellRendererText(), text = columnId)
		column.set_resizable(True)		
		column.set_sort_column_id(columnId)
		self.contactos.append_column(column)
	#-------------------------------------------------------------------------------
	#Método para visualizar el contacto recién ingresado---------------------------
	def contacto(self,id):
		self.lista.clear()
		cursor.execute("SELECT * FROM Victimas WHERE id = '"+id+"'")
		query = cursor.fetchall()
		[self.lista.append([x[0],x[1],x[2],x[3]]) for x in query]
	#----------------------------------------------------------------------------------------------------	
	
	#Método para visualizar en el treeview los contactos.. dependera de la cantidad de contactos-----------
	def todos(self,num):
		self.lista.clear()
		self.num = num
		self.num2 = self.num + 9
		self.label.set_text("Contactos "+str(self.num)+" hasta "+str(self.num2)+"")
		sql='SELECT * FROM Victimas'
		cursor.execute( sql )
		query = cursor.fetchall()
		if query == []:
			self.error("No se encuentran mas datos")
			self.blanco()
		else:
			[self.lista.append([(x[0]),x[1],x[2],x[3]]) for x in query]
	#--------------------------------------------------------------------------------------------------------		
	#Métodos para visualizar treeview de contactos. todos, atras y siguiente.	
	#Permite visualizar de 10 en 10 los resultados de sqlite3 de la tabla contactos.
	def todos2(self, *args):
		self.todos(1)
	
	def todos3(self, *args):
		if self.num == 1:
			num = 1
		else:
			num = self.num - 10
		self.todos(num)
	
	def todos4(self, *args):
		self.todos(self.num + 10)
	#--------------------------------------------------------------------------	

			
		
	#Método para colocar los widgets en blanco----------------------
	def blanco(self):
		self.id.set_text("0")
		self.nombre.set_text("")
		self.muerte.set_text("")
		self.profesion.set_text("")

	#----------------------------------------------------------------
		
	#Método para llenar los campos que vienen de contactos
	def copiaContactos(self, widget):
		i, j = self.contactos.get_selection().get_selected()
		self.idcontactos = i.get_value(j,0)
		self.id.set_text(str(self.idcontactos))
		cursor.execute("SELECT * FROM Victimas WHERE id = %s", (self.idcontactos)) 
		query = cursor.fetchone()
		self.nombre.set_text(str(query[1]))
		self.profesion.set_text(str(query[2]))
		self.muerte.set_text(str(query[3]))
	#-----------------------------------------------------	

	#Método para agregar/moficar contactos-----------------------------------------------
	def agregar_modificar(self, tipo):
		if tipo == 1:
			query= "SELECT * FROM Victimas WHERE id=(SELECT MAX(id) FROM Victimas)"
			cursor.execute(query)
			registros= cursor.fetchone()
			numero=registros[0]
			numero = numero+1
			sql='INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES ("%d","%s","%s","%s")'%(numero,self.nombre.get_text(),self.profesion.get_text(),self.muerte.get_text())
			mensaje = "¿Está seguro que desea agregar a "+self.nombre.get_text()+" "+self.profesion.get_text()
		if tipo == 2:
			sql 	= "UPDATE Victimas SET\
					  nombre = '"+self.nombre.get_text()+"', profesion = '"+self.profesion.get_text()+"',\
					  muerte= '"+self.muerte.get_text()+"'\
					  WHERE id = '"+self.id.get_text()+"'"
			mensaje = "¿Está seguro que desea moficar a "+self.nombre.get_text()+" "+self.profesion.get_text()
		if self.nombre.get_text() == "" or self.profesion.get_text() == "" or self.muerte.get_text() == "":
			self.error(" No se puede agregar/modificar ya que \n Algún campo está en blanco \n El correo es inválido \n El celular tiene menos de 7 digitos\n Ya existe el número telefónico")
		else:
			dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,\
			gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,mensaje)
			if dialog.run() == gtk.RESPONSE_YES:
				cursor.execute(sql)
				if cursor.rowcount < 1:
					self.error("Error al modificar debe seleccionar el contacto de la lista")
				else:
					Conexion.commit()
					self.todos(1)
					self.blanco()
					dialog.destroy()
			else:
				self.aviso("No hay cambios...")
				dialog.destroy()

	#---------------------------------------------------------------------------
	#Métodos para identificar en el método agregar_modificar si se insertan o se modifican contactos
	def agregar(self, *args):
		self.agregar_modificar(1)
	
	def modificar(self, *args):
		self.agregar_modificar(2)
	#-------------------------------------------------------------------------------------------------
	
	#Método para borrar contactos---------------
	def borrar(self, *args):
		if int(self.id.get_text()) == 0:
			self.error("Para borrar necesita seleccionar un contacto de la lista")
		else:
			mensaje = "¿Está seguro que desea borrar al contacto "+self.nombre.get_text()+" "+self.profesion.get_text()+""
			dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,\
			gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,mensaje)
			if dialog.run() == gtk.RESPONSE_YES:
				cursor.execute("DELETE FROM Victimas WHERE id = %s", (self.id.get_text()))
				if cursor.rowcount < 1:
					self.error("Error al borrar al contacto ")
				else:
					Conexion.commit()
					dialog.destroy()
					self.todos(1)
					self.blanco()
			else:
				self.aviso("No hay cambios...")
				dialog.destroy()
			
	#-------------------------------------------
	
	#Método que nos indica si queremos cerrar la ventana-----------------------
	def cerrar(self, *args):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,\
		gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,"¿Está seguro que desea salir?")
		if dialog.run() == gtk.RESPONSE_YES:
			ret = gtk.main_quit()
		else:
			ret = 1
			dialog.destroy()
		return ret
	#---------------------------------------------------------------------------

	#Método para que aparezca un diálogo de advertencia-------------------------------
	def aviso(self, mensaje, *args):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,\
		gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,mensaje)
		dialog.run()
		dialog.destroy()
	#----------------------------------------------------------------------------------
	
#Método para que aparezca un diálogo de error------------------------------
	def error(self, mensaje, *args):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,\
		gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,mensaje)
		dialog.run()
		dialog.destroy()
	#----------------------------------------------------------------------------------
	
	#Método para que aparezca un diálogo de información (querys)-------------------------------
	def informacion(self, mensaje, *args):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,\
		gtk.MESSAGE_INFO, gtk.BUTTONS_OK,mensaje)
		dialog.run()
		dialog.destroy()
	#----------------------------------------------------------------------------------
	
	


if __name__ == "__main__":
	ejercicio2 = Ejercicio2()
	gtk.main()
