# Tarea1-IEE2714
Repositorio de códigos e imágenes (y demás) usados para el desarrollo de la tarea 1.  

## Pregunta 1

En el archivo $\verb*|P1SaturaciónTono.py|$ se encuentra el código listo para ejecutarse con las 3 configuraciones usadas en el informe ya definidas. 

```ruby
puntos_azules = np.array([[0.0, 0.7], 
                   [20.0, 0.6], 
                   [30.0, 0.8], 
                   [50.0, 1.0], 
                   [90.0, 1.0], 
                   [120.0, 1.8], 
                   [150.0, 2.0], 
                   [200.0, 3.0],
                   [210.0, 3.0],
                   [240.0, 2.3], 
                   [250.0, 1.6], 
                   [300.0, 1.0],
                   [350.0, 0.8]])

puntos_rojos = np.array([ [0.0, 3.0],
                   [20.0, 2.6], 
                   [30.0, 2.2], 
                   [50.0, 1.6], 
                   [90.0, 1.0], 
                   [120.0, 1.0], 
                   [150.0, 1.0], 
                   [200.0, 1.0],
                   [210.0, 1.0],
                   [240.0, 1.0], 
                   [250.0, 1.0], 
                   [300.0, 2.5],
                   [350.0, 2.8]])

puntos_amarillos = np.array([ [0.0, 1.0],
                   [20.0, 0.9], 
                   [30.0, 0.5], 
                   [50.0, 0.3], 
                   [90.0, 0.6], 
                   [120.0, 1.0], 
                   [150.0, 1.0], 
                   [200.0, 1.0],
                   [210.0, 1.0],
                   [240.0, 1.0], 
                   [250.0, 1.0], 
                   [300.0, 1.0],
                   [350.0, 1.0]])

imagen = cv2.imread(" Path a la imagen deseada ")
imagenRGB = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
imagen_saturada = ColorSaturation(imagenRGB, '''configuracion deseada''' , '''HSI"/"LCH''')
plt.imshow(imagen_saturada)
plt.show()
```

>        El formato de las configuraciones m(h) debe ser [[h_i, m_i], ...] con h_i < h_{i+1}

Con el path correcto, simplemente se ejecuta el código. 

### Imagenes usadas en el informe

Dentro del repositorio se encuentran la carpeta de imagenes que se usaron para el informe y sus resultados principales (imagenes modificadas).

### Graficos de Configuraciones $m(h)$

Para obtener los graficos de las curvas $m(h)$ se usa el archivo $\verb*|pruebainterp.py|$ donde tambien están definidas las configuraciones usadas. 

```ruby 
puntos_azules = np.array([[0.0, 0.7], 
                   [20.0, 0.6], 
                   [30.0, 0.8], 
                   [50.0, 1.0], 
                   [90.0, 1.0], 
                   [120.0, 1.8], 
                   [150.0, 2.0], 
                   [200.0, 3.0],
                   [210.0, 3.0],
                   [240.0, 2.3],    
                   [250.0, 1.6], 
                   [300.0, 1.0],
                   [350.0, 0.8]])


puntos_rojos = np.array([ [0.0, 3.0],
                   [20.0, 2.6], 
                   [30.0, 2.2], 
                   [50.0, 1.6], 
                   [90.0, 1.0], 
                   [120.0, 1.0], 
                   [150.0, 1.0], 
                   [200.0, 1.0],
                   [210.0, 1.0],
                   [240.0, 1.0], 
                   [250.0, 1.0], 
                   [300.0, 2.5],
                   [350.0, 2.8]])


puntos_amarillos = np.array([ [0.0, 1.0],
                   [20.0, 0.9], 
                   [30.0, 0.5], 
                   [50.0, 0.3], 
                   [90.0, 0.6], 
                   [120.0, 1.0], 
                   [150.0, 1.0], 
                   [200.0, 1.0],
                   [210.0, 1.0],
                   [240.0, 1.0], 
                   [250.0, 1.0], 
                   [300.0, 1.0],
                   [350.0, 1.0]])

graficar_puntos_control(''' Configuración deseada ''')
```

Simplemente se la entrega a la función y se ejecuta el código. 