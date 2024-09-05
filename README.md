El código creado nos ayuda a filtrar una señal de una voz, que se encuentra contaminado por el ruido ambiente y ruido producido por más voces.

Configuración del sistema 

En la habitación,  Ana, Carlos, y Beto, se dispusieron en las esquinas formando un triángulo , con una distancia de 1.5 metros entre ellos. Esta distribución  fue clave para que las voces de todos se puedan escuchar en cada audio, pero que de igual manera sea fácil entender lo que cada uno dice en el.
En relación a los micrófonos cada uno de ellos se coloco en una esquina del triangulo es decir al frente de las personas, a una distancia de ellas de 30 cm, esto con el fin de que no se escuche de mas la respiración y otro tipo de ruidos que produce el cuerpo que no es de nuestro interés, también tuvimos en cuenta que la altura del micrófono fuera igual a la altura de la boca de la persona para asi capturar en un menor porcentaje el ruido del techo o del suelo.

Esta configuración permitió que, aunque las voces se superpusieran ligeramente en los micrófonos, en python se pudo separar de la mejor manera las voces, resaltando la voz de interes, demostrando así la eficacia del experimento.

1. Se grabó el ruido ambiente de la sala y el video duro 7 segundos.
![84d49238-682b-45a6-9d09-af9436fbb2a3](https://github.com/user-attachments/assets/57e84fc6-88f9-49cc-a96b-89c718760eb9)

2. Se grabó a tres personas hablando  ubicadas en diferentes puntos de la sala al tiempo con micrófonos diferentes y todos con una frecuencia de  44khz, cada uno de ellos hablo por 7 segundos, como tenemos 2 bytes, nuestro nivel de cuantificacion es decir nuestros bits por frecuencia son 16 bits por muestra y solo tenemos un canal por lo que es mono.

Para analizar el espectro de todas las señales hicimos un análisis en el dominio de la frecuencia por medio de la transformada de Fourier (FFT), que es utilizada para convertir las señales del dominio del tiempo al dominio de la frecuencia. Esto te permite identificar las frecuencias presentes en la señal, algo crítico para la identificación y filtrado de la voz en el rango de 300 a 3400 Hz. Nuestro codigo grafica el espectro de frecuencias de cada fuente separada, permitiendo visualizar la distribución de las frecuencias de cada señal, lo que es esencial para analizar el contenido frecuencial y aislar la voz principal.

las escalas que utilizamos son:
Lineales: Cuando graficamos las señales en el dominio del tiempo, ya que estamos utilizando una escala lineal para mostrar la amplitud de la señal.
Logarítmicas: cuando realiazamos un análisis del nivel de las señales (dB) y la relación señal-ruido (SNR),lo cual es apropiado ya que los niveles de sonido suelen abarcar un rango dinámico.

3. Se realizó la transformada discreta de Fourier para realizar el análisis espectral de el ruido ambiente, donde en el eje horizontal (x) tenemos la frecuencia  en (Hz) que va desde 0 aun poco mas de los 20,000 Hz y en el vertical (y) tenemos la magnitud que va de 0 a 9, podemos visualizar que la mayor parte de la energía en el espectro esta en las frecuencias mas bajas y esto indica que el ruido que se capto fue fuerte, y vemos como a medida que aumentas las frecuencias se disminuye la señal, y muestra que después de los 10,000 Hz ya no hay energía y esto esta bien ya que asi deben ser las caracterizaciones de la señal del ruido ya que no tienen mucha frecuencia.
   
![20778113-6587-4719-83cc-0cf28efc64fb 2](https://github.com/user-attachments/assets/990e333e-98c0-4202-a064-0680e0e839bf)

4.  Luego se graficaron la señales de los tres audios juntos, en el eje (x) tenemos la cantidad de muestras y tenemos una cantidad total de 270,000 muestras, estas están en función del tiempo. En el eje (y) tenemos a la amplitud y observamos que esta en un rango aproximado de -6 a +6 y podemos observar como la señal 3 es la mas notable en términos de amplitud lo que significa que tiene mas cantidad de información.
   
![22b089ce-dcc1-462e-b4c6-2f32fb282277](https://github.com/user-attachments/assets/4646e225-7723-4103-91b6-24fded8cf819)

5.   Luego se realizó la transformada discreta de Fourier para realizar el análisis espectral de cada señal por separado
1. Fuente 1 (Rojo): El espectro muestra una concentración significativa de energía en frecuencias bajas, principalmente entre 0 y 2,000 Hz, con algunos picos que llegan hasta los 5,000 Hz. Esto sugiere que esta señal podría estar compuesta principalmente por frecuencias bajas, lo cual es común en sonidos donde las frecuencias más bajas corresponden a las vocales o el sonido grave de la voz. A partir de los 5,000 Hz, la magnitud disminuye considerablemente, y casi no hay energía en frecuencias superiores a 10,000 Hz.
2. Fuente 2 (Verde): Esta señal tiene un espectro concentrado también en las frecuencias bajas, especialmente entre 0 y 1,000 Hz, lo que indica que es una señal aún más grave en comparación con la Fuente 1. Después de los 1,000 Hz, la energía de la señal se reduce drásticamente, con solo pequeñas contribuciones hasta los 5,000 Hz. No hay mucha energía en frecuencias más altas (más allá de los 10,000 Hz).
3. Fuente 3 (Azul): La Fuente 3 tiene un espectro más amplio, con un rango significativo de energía entre 0 y 3,000 Hz, y algunos picos menores hasta los 5,000 Hz. es más parecido al de la Fuente 1. Las frecuencias más allá de los 10,000 Hz tienen una magnitud cercana a cero, lo que indica que la señal no tiene contenido relevante en las frecuencias más agudas.
   
![f9abb185-3d43-48ff-9b92-f674734bc81c](https://github.com/user-attachments/assets/c91131ec-1118-4c6a-8a78-2f1275c3eaab)

6. Luego graficamos por separado cada señal para apreciarlas mejor, para separarlas tuvimos que hacer un análisis ya que en el dominio del tiempo, las señales de audio se observan como variaciones de amplitud en función del tiempo. nuestro código grafica estas señales y las separa en tres fuentes distintas tras aplicar ICA. Esto permite observar cómo cambia la amplitud de las señales a lo largo del tiempo.
Las señales de audio filtradas y las originales se normalizan, lo que ayuda a hacer comparaciones consistentes entre ellas en el tiempo.
Análisis en el dominio de la frecuencia:

    
 ![6aeeaae1-2332-401b-b327-e630848847f0](https://github.com/user-attachments/assets/89daf9ed-7fba-4ae5-8faa-85b88847bc64)
![63d148fb-d1a3-44e3-8b20-2c569c94c4bc 2](https://github.com/user-attachments/assets/1b09d6d7-354f-4d68-a06d-db071c6bfa6b)
![792c77e5-923f-4c84-8a63-a32f41e6c456](https://github.com/user-attachments/assets/4018791c-377c-40c7-956e-040f2fdb045e)

7. Nuestra persona de interés fue la numero 2 por ende le agregamos un filtro y la graficamos La señal filtrada presenta una reducción significativa en la amplitud. Ahora oscila entre aproximadamente -0.35 y 0.35 unidades, lo cual indica que se han eliminado muchas de las componentes de frecuencia que existían en la señal sin filtrar, pero se mantiene el numero de muestras , lo que significa que el filtro fue efectivo en eliminar las otra voces y el ruido.
    
 ![42696c68-1e61-40c1-88e2-1769d07a61b8 2](https://github.com/user-attachments/assets/1f572ff3-69f4-46d1-98dd-d582ef310e5d)

8. Se realizo el análisis espectral de la señal luego de ser filtrada y observamos lo siguiente: El eje (x) está marcado en Hertz (Hz), lo que indica la frecuencia de las componentes de la señal en un rango desde 0 Hz hasta aproximadamente 22,000 Hz El eje (y) representa la magnitud de cada componente de frecuencia, que es una medida de la fuerza o amplitud de esa frecuencia en la señal. Las magnitudes varían desde 0 hasta un máximo de aproximadamente 700 unidades. En el rango de 500 Hz a 2000 Hz  hay varios picos en el espectro, aunque las magnitudes son mucho menores (por debajo de 100 unidades).en el rango de 2000 Hz a 5000 Hz Se observa un descenso gradual en la magnitud de las componentes de frecuencia, las magnitudes son todavía menores, y van de valores por debajo de las 50 unidades.
    
 ![220c39f7-e7a7-4ff3-9994-e29b9af717e2 2](https://github.com/user-attachments/assets/45c00967-c2d5-4f56-aa62-c58bce393fc2)

9.  Se cálculo el dB de todas las señales por separadas y nos dieron para la voz 1 -20,26 dB, para la voz 2 -19,28 dB, y para la voz 3 -20,45 dB y luego de filtrar la voz 2 tuvimos -26,12 dB Esta disminución en dB indica que la energía de la señal ha disminuido después del filtrado.
    
12. Se calculó el SNR de todas las señales incluyendo la del ruido y observamos que para todas las señales al ser positivo el resultado es mas fuerte la voz que el ruido ambiente, y en relacion al SNR del ruido ambiente tuvimos 0 dB lo que significa que la potencia de la señal y la potencia del ruido son exactamente iguales. y para saber la calidad, tenemos estos valores:

SNR > 60 dB: Excelente calidad de audio, normalmente indetectable para el oído humano el ruido presente.

SNR entre 40 dB y 60 dB: Buena calidad de audio, el ruido puede ser perceptible pero no molesto.

SNR entre 20 dB y 40 dB: Calidad de audio aceptable, el ruido es perceptible y puede ser molesto en algunas situaciones.

SNR < 20 dB: Mala calidad de audio, el ruido es muy perceptible y afecta significativamente la experiencia de escucha.
podemos ver que el SNR que tenemos para las señales es 42 a 68 dB por ende la calidad del audio es excelente, y en el ruido tenemos que es 0 dB lo que es correcto ya que es una señal de solo ruido.

![7edfbdf3-a563-4b52-89cc-0139403a3419](https://github.com/user-attachments/assets/00d6b864-8408-4222-b118-cff766d9fd5a)

    
10.  Por ultimo lo que se hizo fue reproducir el audio filtrado de la persona numero 2 y este se puede escuchar al finalizar la compilacion de todos los gráficos.

¿Cómo afecta la posición relativa de los micrófonos y las fuentes sonoras en la
efectividad de la separación de señales?
La ubicación de los micrófonos juega un papel crucial en la calidad de la grabación y en el éxito del proceso de filtrado. Si los micrófonos se colocan demasiado cerca entre sí, cada uno captará con mayor intensidad el ruido de las voces de las otras personas, lo que complicará significativamente el proceso de separación y filtrado de las señales. Esto podría generar interferencias que dificulten la distinción clara de cada voz. Por otro lado, si los micrófonos se colocan demasiado lejos, se corre el riesgo de que no todas las voces sean captadas con suficiente claridad por cada micrófono, lo que reduciría la efectividad del experimento. En este caso, habría menos señales relevantes que filtrar, lo cual comprometería los resultados y haría que el esfuerzo no valga la pena. Por tanto, es fundamental encontrar un equilibrio adecuado en la posición de los micrófonos para garantizar una captura óptima del audio y maximizar la eficacia del filtrado.

¿Qué mejoras implementaría en la metodología para obtener mejores
resultados?
Consideraría implementar algunas mejoras en la configuración del cuarto insonorizado. En primer lugar, aumentaría el tamaño del cuarto para evitar que las voces más fuertes de algunas personas se capten con mayor intensidad en los micrófonos, lo que podría generar desequilibrios en la grabación y afectar la precisión del proceso de filtrado. Al proporcionar un espacio más grande, se reduciría la posibilidad de que las voces más fuertes dominen la captura de audio en detrimento de las voces más suaves. Además, sería ideal contar con un sistema de adquisición de audio de mayor calidad, lo que permitiría una captura más precisa y nítida de las señales de voz, mejorando el procesamiento posterior. Estas mejoras podrían marcar una gran diferencia en la calidad del experimento y sus resultados.







