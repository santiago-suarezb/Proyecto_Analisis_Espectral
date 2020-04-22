# -*- coding: utf-8 -*-
"""
@author: Daniel Duque Urrego, Santiago Suárez Bustamante
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.figure import Figure
from PyQt5.uic import loadUi
from numpy import arange, sin, pi
from matplotlib.backends. backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import scipy.io as sio
import numpy as np
from chronux.mtspectrumc import mtspectrumc
from Modelo import Biosenal
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import pywt
# clase con el lienzo (canvas=lienzo) para mostrar en la interfaz los graficos matplotlib, 
#el canvas mete la grafica dentro de la interfaz
class MyGraphCanvas(FigureCanvas):
    '''
    Clase con el lienzo Canvas = Lienzo que permite mostrar en la interfaz los graficos.
    '''
    def __init__(self, parent= None,width=5, height=4, dpi=100):
        '''
        Contructor
        '''
        #se crea un objeto figura
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #el axes en donde va a estar mi grafico debe estar en mi figura
        self.axes = self.fig.add_subplot(111)
        #llamo al metodo para crear el primer grafico
        self.compute_initial_figure()
        #se inicializa la clase FigureCanvas con el objeto fig
        FigureCanvas.__init__(self,self.fig)
        
    def compute_initial_figure(self):
        '''
        Método que se encarga de graficar la función por defecto que aparecerá
        en los dos espacios de graficación, sin embargo, no es la encargada de
        graficar las señales en cuestión.
        '''
        # Se define la frecuencia fundamental
        Fo = 60
        Tp = 1 / Fo
        Fs = 1000
        # Se define la frecuancia de muestreo
        T = 1 / Fs
        A = 5
        t = np.arange(0, 10 * Tp + T, T)
        x = A * np.sin(2 * np.pi * Fo * t)
         # Se calcula la transformada discreta de Fourier
        DFT = fft(x)
        N = len(DFT)
        # Se toma y grafica solo la mitad pues es simétrica
        Nmitad = int(np.ceil(N / 2))
        Fmitad = np.arange(0, Nmitad) * Fs / N
        DFTmitad = DFT[0:Nmitad]
        self.axes.plot(Fmitad,np.abs(DFTmitad),'k')
        self.axes.set_title("DFT señal sinusoidal 60 Hz")
        self.axes.set_xlabel("Frecuencia (Hz)")
        self.axes.set_ylabel("Amplitud")
        
    def graficar_gatos(self,datos, legend):
        '''
        Función graficar gatos, se encarga de gaficar cada uno de los canales 
        que se detectan de la señal cargada, de manera distanciada y diferenciados
        por color, como variables de entrada, recibe los datos que se graficarán.
        '''
        #Se limpia el espacio de graficación
        self.axes.clear()
        #Se ingresan los datos que van a ser graficados
        #self.axes.plot(datos)

        #El siguiente cilo, permite graficar cada uno de los canales detectados, 
        #distanciándolos para evitar superposiciones y ayudar a la mejor visualización.
        for i in range(datos.shape[0]):
            self.axes.plot(datos[i], linewidth=0.8)
        self.axes.set_xlabel("Tiempo")
        self.axes.set_ylabel("Amplitud")
  
        #Se dibuja cada canal y se añade una leyenda para diferenciar los canales. 
        self.axes.legend(legend)
        self.axes.figure.canvas.draw()
        
    def graficar_canal(self,datos,canal_seleccionado, x_min, x_max, fs):
        '''
        La función graficar canal, es la encargada de hacer la respectiva gráfica
        del canal seleccionado por el usuario. Como variables de entrada, recibe 
        los datos completos de la señal y el índice del combo box que indica el canal
        que se desea graficar, además de la frecuencia de muestreo establecida por el
        usuario y los límites de graficación del eje independiente.
        '''
        self.axes.clear()
        inicio = x_min / fs
        final = x_max / fs
        # Se calcula el periodo de muestreo con el objetivo de graficar respecto al tiempo
        sampling_period =  1 / fs
        # Se crea el vector tiempo
        time = np.arange(inicio, final, sampling_period)
        datos = datos[canal_seleccionado, :]
        time = time[(time >= inicio) & (time <= final)]
        # Se grafica
        self.axes.plot(time, datos, 'k',linewidth=0.5)

        
        #Se establecen el título general y los títulos de los ejes.
        self.axes.set_title("Señal seleccionada")
        self.axes.set_xlabel("Tiempo (s)")
        self.axes.set_ylabel("Amplitud")
        self.axes.set_autoscale_on(True)

        #Se ordena la graficación del canal 
        self.axes.figure.canvas.draw()
    
    def graficar_w(self, f, pxx):
        '''
        Método que permite realizar la respectiva gráfica porterior al análisis de Welch o 
        Multitaper, recibe los retornos de ambas funciones que son f y Pxx.
        '''
        # Se limpia el gráfico anterior
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title("Análisis seleccionado")
        self.axes.set_xlabel("Frecuencia (Hz)")
        self.axes.set_ylabel("Amplitud")
        self.axes.set_autoscale_on(True)
        self.axes.plot(f, pxx, 'k')
        self.axes.figure.canvas.draw()
        
    def graficar_espectro(self, time, freqs, power, f_min, f_max, t_min, t_max):
        '''
        Método que permite realizar el diagrama de Wavelet continuo, recibe el tiempo, frecuencia
        y potencia provenientes de la función graficacion_wavelet, así como los límites de tiempo y 
        frecuencia que se desean graficar.
        '''
        #primero se necesita limpiar la grafica anterior
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        #ingresamos los datos a graficar
        scalogram = self.axes.contourf(time[t_min:t_max],
                 freqs[(freqs >= f_min) & (freqs <= f_max)],
                 power[(freqs >= f_min) & (freqs <= f_max), t_min:t_max],
                 100, # Especificar 20 divisiones en las escalas de color 
                 extend='both')
        self.axes.set_ylabel('frequency [Hz]')
        self.axes.set_xlabel('Time [s]')     
        #Se ordena la graficación de la escala de colores correspondiente al escalograma
        self.bcr = self.fig.colorbar(scalogram, ax=self.axes)
        #ordenamos que dibuje
        self.fig.canvas.draw()

            
#%%

class InterfazGrafico(QMainWindow):
    '''
    Clase InterfazGrafico, se define para crear la interfaz gráfica
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        super(InterfazGrafico,self).__init__()
        #Se carga el diseño creado.
        loadUi ('anadir_grafico.ui',self)
        #Se llama la rutina donde configuramos la interfaz
        self.setup()
        #Se muestra la interfaz
        self.showMaximized()

        #Se crea bandera para saber si se ha ejecutado algún método de análisis
        #frecuencia
        self.__num_ejecuciones_frec = 0
        
        #Se crea bandera para saber si se ha ejecutado la wavelet continua
        self.__ej_wavelet = 0
        
    def setup(self):
        '''
        Función setup es la función que permite configurar, habilitar, deshabilitar
        cada uno de los componentes de la interfaz gráfica.
        '''
       
        layout = QVBoxLayout()
        #Se añade el organizador al campo grafico
        self.campo_grafico.setLayout(layout)
        #se crean dos objetos para manejo de graficos originales y filtrados
        #respectivamente
        self.__sc = MyGraphCanvas(self.campo_grafico, width=5, height=4, dpi=100)
        self.__sc_2 = MyGraphCanvas(self.campo_grafico_2, width=5, height=4, dpi=100)
        #Se añade el campo de graficos
        layout.addWidget(self.__sc)
        layout.addWidget(self.__sc_2)
        
        #Se vincula cada uno de los botones pertenecientes a la interfaz con su 
        #finción a realizar.
        self.boton_cargar.clicked.connect(self.cargar_senal)
        self.graficar_senal.clicked.connect(self.mostrar_canal)
        self.escalar_tiempo.clicked.connect(self.escalar_eje_tiempo)
        self.escalar_frecuencia.clicked.connect(self.escalar_eje_frecuencia)
        self.analizar_welch.clicked.connect(self.graficar_welch)
        self.analizar_multi.clicked.connect(self.graficar_multitaper)
        self.comboBox.currentIndexChanged.connect(self.cambio_combo)
        self.combo_metodo.currentIndexChanged.connect(self.opcion_metodo)
        self.graficar_wavelet.clicked.connect(self.graficacion_wavelet)
        self.window_multi_fin.valueChanged.connect(self.ajustar_parametro)
        self.bw.valueChanged.connect(self.ajustar_parametro)
        self.t.valueChanged.connect(self.ajustar_parametro)
        self.p.valueChanged.connect(self.ajustar_parametro)
        
        self.check_DC.setChecked(True)
        self.emergente = QMessageBox()
        
        #Se des habilitan los botones que no deben estar activos para la primer acción
        #es decir, para cargar la señal, cuando la señal se cargue se activarán.
        self.comboBox.setEnabled(False)
        self.escalar_tiempo.setEnabled(False)
        self.escalar_frecuencia.setEnabled(False)
        self.frecuencia_inicial.setEnabled(False)
        self.frecuencia_final.setEnabled(False)
        self.graficar_senal.setEnabled(False)
        self.check_DC.setEnabled(False)
        self.tiempo_inicial.setEnabled(False)
        self.tiempo_final.setEnabled(False)
        self.combo_metodo.setEnabled(False)
        self.window_welch.setEnabled(False)
        self.porcent.setEnabled(False)
        self.analizar_welch.setEnabled(False)
        self.bw.setEnabled(False)
        self.t.setEnabled(False)
        self.p.setEnabled(False)
        self.analizar_multi.setEnabled(False)
        self.window_multi_fin.setEnabled(False)
        self.parameter.setEnabled(False)
        self.graficar_wavelet.setEnabled(False)
        self.radio_wavelet.setEnabled(False)
        self.radio_senal.setEnabled(False)
        self.fs.setEnabled(False)
    
    def ajustar_parametro(self):
        '''
        Método para agregar sugerencias de parámetros para la partición de la
        señal en el método de análisis de multitaper
        '''
        if (self.window_multi_fin.value()!= 0 and self.bw.value()!= 0 and self.t.value()!= 0 and self.p.value()!= 0):
            self.parameter.clear()
            for i in range(self.__num_datos):
                if (self.__num_datos % (self.fs.value() * (i + 1)))==0:
                    self.parameter.addItem(str(i + 1))
    
    def cambio_combo(self):
        '''
        Método que permite desactivar ma mayoría de botones y campos cuando se realice un 
        cambio en la elección del canal que se desea graficar, de manera que no genere bucles
        o conflictos.
        '''
        self.check_DC.setEnabled(False)
        self.combo_metodo.setEnabled(False)
        self.window_welch.setEnabled(False)
        self.porcent.setEnabled(False)
        self.analizar_welch.setEnabled(False)
        self.bw.setEnabled(False)
        self.t.setEnabled(False)
        self.p.setEnabled(False)
        self.analizar_multi.setEnabled(False)
        self.window_multi_fin.setEnabled(False)
        self.parameter.setEnabled(False)
        self.graficar_wavelet.setEnabled(False)
        self.radio_wavelet.setEnabled(False)
        self.radio_senal.setEnabled(False)
        self.escalar_frecuencia.setEnabled(False)
        self.frecuencia_inicial.setEnabled(False)
        self.frecuencia_final.setEnabled(False)
        
    def opcion_metodo(self):
        '''
        Método que se define para activar o inactivar los campos que reciben los valores para Welch y 
        multitaper, se habilitará dependiendo del índice seleccionado en un comboBox.
        '''
        opcion = self.combo_metodo.currentIndex()
        # Índice 0 activa los campos correspondientes a Welch
        if opcion==0:
            self.window_welch.setEnabled(True)
            self.porcent.setEnabled(True)
            self.analizar_welch.setEnabled(True)
            self.bw.setEnabled(False)
            self.t.setEnabled(False)
            self.p.setEnabled(False)
            self.analizar_multi.setEnabled(False)
            self.window_multi_fin.setEnabled(False)
            self.parameter.setEnabled(False)
            self.radio_wavelet.setEnabled(False)
            self.radio_senal.setEnabled(False)
            self.escalar_frecuencia.setEnabled(False)
        # Índice 1 activa los campos correspondientes a Multitaper
        else:
            self.window_welch.setEnabled(False)
            self.porcent.setEnabled(False)
            self.analizar_welch.setEnabled(False)
            self.bw.setEnabled(True)
            self.t.setEnabled(True)
            self.p.setEnabled(True)
            self.analizar_multi.setEnabled(True)
            self.window_multi_fin.setEnabled(True)
            self.parameter.setEnabled(True)
            self.radio_wavelet.setEnabled(False)
            self.radio_senal.setEnabled(False)
            self.escalar_frecuencia.setEnabled(False)
            
            
    def asignar_Controlador(self,controlador):
        '''
        Método que asigna el controlador.
        '''
        self.__coordinador=controlador
    
    def graficacion_wavelet(self):
        '''
        Método que toma realiza el preproceso de los datos ingresador por el usuario para la 
        graficación del Wavelet continuo, envía los parámetros necesarios al método descrito
        anteriormente como lo son la frecuencia, potencia y tiempo, para la respectiva graficación
        '''
        self.frecuencia_inicial.setEnabled(True)
        self.frecuencia_final.setEnabled(True)
        self.radio_wavelet.setEnabled(True)
        self.escalar_frecuencia.setEnabled(True)
        # Se toma el índice del canal seleccionado
        canal_seleccionado = self.comboBox.currentIndex()
        # Se encuentra el periodo de muestreo por medio del valor puesto en el spinBox
        sampling_period =  1 / self.fs.value()
         # Se realiza el procesamiento que requiere la Wavelet continua
        scales = np.arange(1, self.fs.value())
        frequencies = pywt.scale2frequency('cmor', scales) / sampling_period
        scales = scales[(frequencies >= self.__f_min) & (frequencies <= self.__f_max)]
        time_epoch = sampling_period * self.__num_datos
        time = np.arange(0, time_epoch, sampling_period)
        # Se toman los datos correspondientes al canal seleccionado
        datos = self.__coordinador.devolverDatosSenal(0, self.__num_datos)[canal_seleccionado]
        # Condicional que permite filtrar o no los datos que se van a graficar, esto se hace por
        #medio de la validación de un cuadro de confirmación, al estar confirmado quiere decir que.
        #se debe retirar el nivel DC restando la media.
        if self.check_DC.isChecked() == True:
            datos = datos - np.mean(datos)
        # Se toman los coeficientes y la frencuencia entregados por la función
        [coef, freqs] = pywt.cwt(datos, scales, 'cmor', sampling_period)
         # Se llama la función graficar espectro definida en línas anteriores.
        power = (np.abs(coef)) ** 2
        self.__sc_2.graficar_espectro(time, freqs, power, self.__f_min, self.__f_max, self.__x_min, self.__x_max)
        # Se activa un botón tipo radio que permite escalar en tiempo y frecuencia el Wavelet continuo.
        self.radio_wavelet.setEnabled(True)
         # Se inicializa una bandera que servirá como verificación
        self.__ej_wavelet = 1
        
        
    
    def escalar_eje_tiempo(self):
        '''
        Función escalar_eje_tiempo, permite recortar el eje tiempo a partir
        de dos botones de selección (Spin Box), donde se especifica el valor inicial
        y el valor final que tomará el nuevo eje, esta función invoca la función definida
        anteriormente graficar canal y se pasan como valor a esta, el rango de tiempo que 
        se desea graficar en s.
        '''
        #Se toma el valor inicial y final del tiempo de los dos Spin Box.
        inicio = int(self.tiempo_inicial.value()) * self.fs.value()
        fin = int(self.tiempo_final.value()) * self.fs.value()
        
        #En el siguiente condicional se comparan los valores de los spin Box, para 
        #evitar que el tiempo inicial sea mayor que el final y si esto sucede, se
        #entrega un mensaje de información.
        if inicio >= fin:
            msg=QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle('Información')
            msg.setWindowIcon(QtGui.QIcon("information.png"))
            msg.setText("RANGO INVÁLIDO.")
            msg.setInformativeText("El tiempo final es mayor al inicial, favor ingresar un rango válido.")
            msg.exec_()
        
       #Si el tiempo inicial no es mayor que el final, se procede a la graficación
        #del rango de tiempo deseado.
        else:
            
            #Se reciben los valores requeridos para escalar igualmente la señal filtrada
            self.__x_min = inicio
            self.__x_max = fin
            canal_seleccionado = self.comboBox.currentIndex()
            #Se escala el canal seleccionado.
            self.__sc.graficar_canal(self.__coordinador.devolverDatosSenal(self.__x_min, self.__x_max),\
                                     canal_seleccionado, self.__x_min, self.__x_max, self.fs.value())
            if self.__ej_wavelet == 1:
                self.graficacion_wavelet()
    
    def escalar_eje_frecuencia(self):
        '''
        Analogamente al método anterior, permite recortar el de frecuencias a partir
        de dos botones de selección (Spin Box), donde se especifica el valor inicial
        y el valor final que tomará el nuevo eje, esta función invoca la función definida
        anteriormente graficar canal y se pasan como valor a esta, el rango de frecuencia que 
        se desea graficar en Hz.
        '''
        inicio = int(self.frecuencia_inicial.value())
        fin = int(self.frecuencia_final.value())
        
        #En el siguiente condicional se comparan los valores de los spin Box, para 
        #evitar que la frecuencia inicial sea mayor que la final y si esto sucede, se
        #entrega un mensaje de información.
        if inicio >= fin:
            msg=QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle('Información')
            msg.setWindowIcon(QtGui.QIcon("information.png"))
            msg.setText("RANGO INVÁLIDO.")
            msg.setInformativeText("La frecuencia final es mayor a la inicial, favor ingresar un rango válido.")
            msg.exec_()
        
        #Si la frecuencia inicial no es mayor que el final, se procede a la graficación
        #del rango de tiempo deseado.
        else:
            
            #Se reciben los valores requeridos para escalar igualmente la señal filtrada
            self.__f_min = inicio
            self.__f_max = fin
            if self.fs.value() != 0:
                if self.radio_senal.isChecked():
                    if self.combo_metodo.currentIndex() == 0:
                        self.__num_ejecuciones_frec = 1
                        self.graficar_welch()
                    else:
                        self.__num_ejecuciones_frec = 1
                        self.graficar_multitaper()
                else:
                    self.__num_ejecuciones_frec = 1
                    self.graficacion_wavelet()
           
    def add_canales(self, canales):
        '''
        La función add_canales, se encarga de llenar el Combobox dependiendo de
        la cantidad de canales que se detectan de la señal original, recibe como 
        parámetro la cantidad de filas que se detectan de la señal original (canales)
        '''
        
        lista = map(str, canales)
        #Se añaden los valores a la lista del combo Box
        self.comboBox.clear()
        self.comboBox.addItems(lista)
        
    def mostrar_canal(self):
        '''
        La siguiente función está ligada con el botón graficar señal y permite
        mostrar en el campo gráfico el canal seleccionado por el usuario mediante
        el comboBoX        
        '''
        if self.fs.value()==0:
            msg=QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle('Información')
            msg.setWindowIcon(QtGui.QIcon("information.png"))
            msg.setText("VALOR INVÁLIDO.")
            msg.setInformativeText("El valor de la frecuencia no puede ser 0 Hz")
            msg.exec_()
        else:
            self.combo_metodo.setEnabled(True)
            self.check_DC.setEnabled(True)
            self.fs.setEnabled(True)
            self.tiempo_inicial.setEnabled(True)
            self.tiempo_final.setEnabled(True)
            self.escalar_tiempo.setEnabled(True)
            self.graficar_wavelet.setEnabled(True)
            self.opcion_metodo()
            #Se toma el valor del combo Box.
            canal_seleccionado = self.comboBox.currentIndex()
            #Se determinan los valores del eje independiente.
            self.__x_min=0
            self.__x_max=self.__coordinador.devolverDatosSenal(self.__x_min, self.__x_max).shape[1]
            #Se procede a graficar el canal.
            self.__sc.graficar_canal(self.__coordinador.devolverDatosSenal(self.__x_min, self.__x_max),\
                                     canal_seleccionado, self.__x_min, self.__x_max, self.fs.value())
            sampling_period =  1 / self.fs.value()
            time_epoch = sampling_period * (self.__x_max)
            # Se muestra al usuario el tiempo máximo en pantalla, de igual manera de limita el campo final
            self.label_tiempo.setText('Tiempo máx: {} s'.format(int(time_epoch)))
            self.__f_min = 0
            self.__f_max = self.fs.value()
            self.__ej_wavelet = 0
            self.window_multi_fin.setMaximum(self.fs.value())
    
    def graficar_welch(self):
        '''
        Función encargada de capturar y pre procesar los parámetros que serán entregados a la 
        función encargada de hacer el análisis de Welche.
        '''
        # Condicional que saca un mensaje emergente cuando el tamaño de ventana es 0
        if self.window_welch.value()==0:
            msg=QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle('Información')
            msg.setWindowIcon(QtGui.QIcon("information.png"))
            msg.setText("VALOR INVÁLIDO.")
            msg.setInformativeText("El tamaño de la ventana no puede ser 0")
            msg.exec_()
        else:
            opcion = self.comboBox.currentIndex()
            # Se toma el tamaño de la ventana
            self.window = int(self.window_welch.value())
            # Se calcula el tamaño de solapamiento
            self.superposition = int(self.porcent.value())
            state_DC = self.check_DC.isChecked()
            # Entregamos los parámetros a la función que realizará el procesamiento y graficación
            f, pxx = self.__coordinador.graficar_welch(opcion, self.window,self.superposition, self.fs.value(),\
                                                       state_DC)
            if self.__num_ejecuciones_frec == 0:
                self.__f_min = np.min(f)
                self.__f_max = np.max(f)
            self.__sc_2.graficar_w(f[(f >= self.__f_min) & (f <= self.__f_max)], pxx[(f >= self.__f_min)\
                                     & (f <= self.__f_max)])
             # Se entrega la frecuencia máxima en pantalla, de igual manera se limita el campo final
            self.label_frecuencia.setText('Frecuencia máx: {} Hz'.format(int(f[-1])))
            self.__num_ejecuciones_frec = 0
            self.frecuencia_inicial.setMaximum(np.max(f))
            self.frecuencia_final.setMaximum(np.max(f))
             # Se habilitan los botones que pueden ser usados luego del procesamiento de Welch
            self.radio_wavelet.setEnabled(False)
            self.radio_senal.setEnabled(True)
            self.escalar_frecuencia.setEnabled(True)
            self.frecuencia_inicial.setEnabled(True)
            self.frecuencia_final.setEnabled(True)
            self.__ej_wavelet = 0
        
    def graficar_multitaper(self):
        '''
        Función encargada de capturar y pre procesar los parámetros que serán entregados a la 
        función encargada de hacer el análisis multitaper.
        '''
        opcion = self.comboBox.currentIndex()
        # Se capturan los parámetros
        inicio = 0
        fin = int(self.window_multi_fin.value())
        bw = int(self.bw.value())
        t = int(self.t.value())
        p = int(self.p.value())
        parameter = int(self.parameter.currentText())
        fs = self.fs.value()
        # Condicional que muestra un mensaje emergente cuando el tamaño de banda es 0
        if self.window_multi_fin.value()==0:
            msg=QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle('Información')
            msg.setWindowIcon(QtGui.QIcon("information.png"))
            msg.setText("VALOR INVÁLIDO.")
            msg.setInformativeText("El tamaño de la banda no puede ser 0")
            msg.exec_()
        else:
            if (parameter*fs) > (self.__coordinador.devolverDatosSenal(0,self.__num_datos)[opcion].shape[0]):
                msg=QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowTitle('Información')
                msg.setWindowIcon(QtGui.QIcon("information.png"))
                msg.setText("DATO INVÁLIDO.")
                msg.setInformativeText("El parámetro de partición excede el valor máximo, ingrese un valor menor a {}"\
                                       .format(int(self.__coordinador.devolverDatosSenal(0,self.__num_datos)[opcion]\
                                                   .shape[0]/self.fs.value())))
                msg.exec_()
            else:
                # Se llama la función encargada del procesamiento
                pxx, f = self.__coordinador.graficar_multitaper(opcion, inicio, fin, bw, t, p, parameter, \
                                                                self.fs.value(), self.check_DC.isChecked())
                if self.__num_ejecuciones_frec == 0:
                    self.__f_min = np.min(f)
                    self.__f_max = np.max(f)
                self.__sc_2.graficar_w(f[(f >= self.__f_min) & (f <= self.__f_max)], pxx[(f >= self.__f_min)\
                                         & (f <= self.__f_max)])
                self.label_frecuencia.setText('Frecuencia máx: {} Hz'.format(int(f[-1])))
                self.__num_ejecuciones_frec = 0
                self.frecuencia_inicial.setMaximum(np.max(f))
                self.frecuencia_final.setMaximum(np.max(f))
                 # Se habilitan los botones que pueden ser usados luego del procesamiento multitaper
                self.radio_wavelet.setEnabled(False)
                self.radio_senal.setEnabled(True)
                self.escalar_frecuencia.setEnabled(True)
                self.frecuencia_inicial.setEnabled(True)
                self.frecuencia_final.setEnabled(True)
                self.__ej_wavelet = 0
        
    def cargar_senal(self):
        '''
        La función cargar_señal, es la que posibilita cargar la señal .mat para su
        posterior procesamiento.
        '''
        #se abre el cuadro de dialogo para cargar, de archivos .mat
        archivo_cargado, _ = QFileDialog.getOpenFileName(self, "Abrir señal","","Todos los archivos (*);\
                                                         ;Archivos mat (*.mat)*")
        
        if archivo_cargado != "":
            data = sio.loadmat(archivo_cargado)
            # Se toman las Keys del diccionario que luego serán mostradas en el comboBox
            self.__keys = list(data.keys())
            keys = list(data.keys())
            datos=[]
            keys=[]
            for i in range(len(self.__keys)):
             # El siguiente condicional se encarga de retirar los primero índices que no tienen
             #señales si no datos de la optención y versión
                if np.size(data[self.__keys[i]]) > 1:
                    keys.append(self.__keys[i])
                    datos = np.append(datos, data[self.__keys[i]])
                    
            self.__keys = keys
            datos = np.reshape(datos, (len(self.__keys), data[self.__keys[0]].shape[1]), order='C')
            
            num_senales,num_datos = datos.shape
            # Se invoca al coordinador que recibe los datos
            self.__coordinador.recibirDatosSenal(datos)
            self.__x_min = 0
            self.__x_max = data[self.__keys[0]].shape[1]
            self.__num_datos = data[self.__keys[0]].shape[1]
            #Se grafica por medio del controlador
            self.__sc.graficar_gatos(self.__coordinador.devolverDatosSenal(self.__x_min,self.__x_max), self.__keys)
            #Se habilitan todos los botones, pues ya se tiene una señal para procesar
            self.comboBox.setEnabled(True)
            self.graficar_senal.setEnabled(True)
            self.fs.setEnabled(True)
            self.fs.setEnabled(True)
            #Se garantiza que los spin Box selectores del rango de tiempo, vayan
            #hasta el máximo valor que puede tomar el eje independiente
            self.tiempo_inicial.setMaximum(self.__x_max)
            self.tiempo_final.setMaximum(self.__x_max)
            
            #Se invoca la función que llenará el spin Box.
            self.add_canales(self.__keys)


        
        
        
        
        
        
        