<H1>Análisis Espectral 📖</H1> 

<P ALIGN="justify">El proyecto está enfocado en poder realizar un análisis frecuencial por medio de una interfaz gráfica, en ella el usuario podrá variar 
los parámetros que son requeridos por el proceso Welch y Multitaper, adicional a esto, se podrá dar visualización a un método gráfico
como lo es el Wavelet continuo (tiempo - frecuencia), que consiste en un espectograma con distribución de colores. Además, permite 
retirar el nivel DC que traen algunas señales por defecto, lo que favorece un mejor análisis final.

<H3>Comenzando 🚀 </H3></p>
<b>1.</b> En primer lugar se deben descargar todos los archivos que están publicados, incluido el llamado chronux.zip.</p>
<b>2.</b> Es fundamental tener todos los archivos en la misma carpeta donde se alojó la arquitectura MVC.</p>
<b>3.</b> Las imágenes que se encuentran dentro del archivo son usadas en la interfaz gráfica para mejorar la presentación de esta.</p>
<b>4.</b> El archivo dataset_senales es un arvhivo que contiene 3 señales diferentes que es útil para realizar pruebas al modelo completo.</p>


<H3>Pre-requisitos 📋 </H3></p>
<P ALIGN="justify">El único requerimiento además de tener correctamente instalado Python, es la cartepeta que contiene la librería que es
necesaria para el análisis multitaper.</p>
<P ALIGN="justify">Para esto, se debe descargar el archivo chronux.zip que se encuentra publicado y extraer los archivos; posteriormente,
crear una carpeta que lleve por nombre chronux y finalmente, alojar esta en la misma carpeta donde se encuentra la arquitectura MVC </p>


<H3>Uso de la interfaz 🔧⚙️ </H3></p>
<P ALIGN="justify">Para el uso de la interfaz, luego de hacer realizado correctamente los pasos anteriores, se debe ejecutar el archivo
que tiene por nombre Controlador.py, este desplegará automáticamente la ventana correspondiente a la interfaz y como modo de prueba,
se puede realizar el primer acercamiento con la señal que se encuentra en el paquete del proyecto.</p>
Al ser una interfaz amigable con el usuario simplemente debes seguir los siguientes pasos:</p>
<b>1.</b> Cargar la señal. </p>
<b>2.</b> Seleccionar el canal de la señal a previsualizar e ingresar la frecuencia muestreada (señal ejemplo 250 Hz) </p>
<b>3.</b> Seleccionar en el comboBox análisis, el método que se quiere analizar, llenar los cuadros de parámetros y oprimir el botón
analizar. </p>
<b>4.</b> En el otro panel, se tiene un botón que permite graficar el escalograma de Wavelet solamente dando clic. </p>
<b>5.</b> Finalmente, se tiene la posibilidad de escalar en frecuencia tanto el escalograma como el análisis seleccionado, además de
escalar en tiempo la transformada Wavelet y el canal seleccionado inicialmente.</p>
<b>6.</b> Se puede volver a la selección de otro canal y realizar el mismo proceso o seleccionar otros parámetros para el análisis.

<H3>Validaciones en codificación ⌨️</H3></p>
<P ALIGN="justify"> La interfaz lleva consigo algunas validaciones requeridas para evitar bucles o problemas en la interfaz. </p>
<b>1.</b> Se valida que al escalar tiempo y frecuencia el tiempo final sea mayor al inicial.</p>
<b>2.</b> Se valida que el tamaño de ventana seleccionado en Welch y la banda de frecuencia seleccionada en Multitaper sea diferente
de 0, esto debido a que no presenta sentido físico un tamaño de 0 Hz para el análisis.</p>
<b>3.</b>Se valida que la frecuencia de muestreo difiera de 0.</p>



<H3>Construido con 🛠️</H3></p>
<b>1.</b> Python con su entorno Spider. </p>
<b>1.</b> PyQt (biblioteca gráfica de Python) por medio de la cuál se creó la ventana.</p>


<H3>Autores ✒️ </H3></p>

<b>Daniel Duque Urrego</b> - Trabajo Inicial, Documentación - danielduqueu. </p> 
<b>Santiago Suárez Bustamante</b> - Trabajo Inicial, Documentación - santiago_suarezb </p>


<H3>Licencia 📄</H3></p>
Este proyecto es totalmente gratuito.</p>


<H3>Comenta a otros sobre este proyecto!! 📢</H3>

