# -*- coding: utf-8 -*-
"""
@author: Daniel Duque Urrego, Santiago Suárez Bustamante
"""
from Modelo import Biosenal
from interfaz import InterfazGrafico
import sys
from PyQt5.QtWidgets import QApplication

class Principal(object):
    '''
    Clase Principal, se define para poder enlazar el coordinador, la interfaz
    gráfica y el modelo
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.__app=QApplication(sys.argv)
        self.__mi_vista=InterfazGrafico()
        self.__mi_biosenal=Biosenal()
        self.__mi_controlador=Coordinador(self.__mi_vista,self.__mi_biosenal)
        self.__mi_vista.asignar_Controlador(self.__mi_controlador)
    def main(self):
        '''
        Ejecución de interfaz gráfica
        '''
        self.__mi_vista.show()
        sys.exit(self.__app.exec_())
    
class Coordinador(object):
    '''
    Clase coordinador, se define para conectar la interfaz gráfica
    con el modelo
    '''
    def __init__(self,vista,biosenal):
        '''
        Constructor
        '''
        self.__mi_vista=vista
        self.__mi_biosenal=biosenal
        
    def recibirDatosSenal(self,data):
        self.__mi_biosenal.asignarDatos(data)
        
    def devolverDatosSenal(self,x_min,x_max):
        return self.__mi_biosenal.devolver_segmento(x_min,x_max)
    
    def graficar_welch(self, opcion, ws, ps, fs, state_DC):
        '''
        Conecta los valores obtenidos de la interfaz gráfica con la función que realiza
        el análisis de Welch que está en el modelo. Además del parámetro que permite o no 
        retirar el nivel DC.
        '''
        return self.__mi_biosenal.welch(opcion, ws, ps, fs, state_DC)
    def graficar_multitaper(self, opcion, inicio, fin, bw, t, p, multiply, fs, state_DC):
        '''
        Toma los parámetros provenientes de la interfaz y los pasa como parámetro a la 
        función que se encarga de realizar el análisis multitaper que está en el modelo.
        Además del parámetro que permite o no retirar el nivel DC.
        '''
        return self.__mi_biosenal.multitaper(opcion, inicio, fin, bw, t, p, multiply, fs, state_DC)
p=Principal()
p.main()