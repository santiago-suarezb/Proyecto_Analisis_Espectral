# -*- coding: utf-8 -*-
"""
@author: Daniel Duque Urrego, Santiago Suárez Bustamante
"""
import numpy as np
import scipy.io as sio;
import scipy.signal as signal
from chronux.mtspectrumc import mtspectrumc

class Biosenal(object):
    def __init__(self,data=None):
        '''
        Constructor
        '''
        if not data==None:
            self.asignarDatos(data)
        else:
            self.__data=np.asarray([])
            
    def asignarDatos(self,data):
        self.__data=data

    def devolver_segmento(self,x_min,x_max):
        '''
        Método que me recibe el rango que se desea graficar y me retorna los 
        valores de la señal que están contenidos en dicho rango.
        '''
        #Si el valor inicial es mayor que el final no se retorna nada, se previene
        # errores
        if x_min >= x_max:
            return None
        #Se toman los valores de la señal que están contenidos en el rango de 
        #tiempo seleccionado
        return self.__data[:,x_min:x_max]
    
    def welch(self, opcion, WS, PS, fs, state_DC):
        '''
        Método encargadado de realizar el análsis del método Welch, recibe el tamaño
        de la ventana, el porcentaje de solapamiento, el estado del radio que da orden
        de rertirar el nivel DC y la frecuencia de muestreo y devuelve dos variables 
        (f y Pxx) que luego serán graficadas y será el resultado del análisis.
        '''
        if state_DC == False:
         # Si no se selecciona el filtrado DC
            solapamiento = int((WS*PS)/100)
            f,Pxx = signal.welch(self.__data[opcion], fs ,'hamming', WS, solapamiento, WS, scaling ='density')
        else:
        # Si se selecciona el filtrado DC
            datos = self.__data[opcion]
            # Se quita el promedio del canal seleccionado por medio de la media
            datos = datos - np.mean(datos)
            solapamiento = int((WS*PS)/100)
            f,Pxx = signal.welch(datos, fs ,'hamming', WS, solapamiento, WS, scaling ='density')
        return [f,Pxx]
    
    def multitaper(self, opcion_senal, inicio, fin, bw, t, p, multiply, fs, state_DC):
        '''
        Función que tiene como objetivo realizar el análisis del método multitaper, 
        recibe la banda de paso que se va a analizar y los parámetros W (frec. cercanas)
        T (tiempo de duración de la ventana) ,P(cantidad de ventanas ortogonales) y el
        factor que da indicios de la cantidad de segmentos que se tomarán, que son
        necesarios para este modelo y devuelve finalmente los parámetros de frecuencia
        y valores que darán el gráfico del resultado.
        '''
        if state_DC==False:
            params = dict(fs = fs, fpass = [inicio, fin], tapers = [bw, t, p], trialave = 1)
            # Se mantiene la relación para garantizar los valores correctos para el reshape
            x = int(self.__data[opcion_senal].shape[0]/(fs*multiply))
            datos = self.__data[opcion_senal]
            datos = datos[:fs*multiply*x]
            data = np.reshape(datos, (fs*multiply, x),order='F')
            Pxx,f = mtspectrumc(data, params)
        else:
            datos = self.__data[opcion_senal]
            datos = datos - np.mean(datos)
            params = dict(fs = fs, fpass = [inicio, fin], tapers = [bw, t, p], trialave = 1)
            x = int(datos.shape[0]/(fs*multiply))
            datos = datos[:fs*multiply*x]
            data = np.reshape(datos, (fs*multiply, x),order='F')
            Pxx,f = mtspectrumc(data, params)
        return Pxx,f