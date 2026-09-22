import matplotlib.pyplot as plt
import cv2
import numpy as np




def Reescalado(imagenRGB: np.ndarray, s:float, interp: str):

    filas_M, columnas_N = imagenRGB.shape[:2]
    filas_salidaM, columnas_salidaN = int(np.floor(filas_M*s)), int(np.floor(columnas_N*s))
    sy_real, sx_real = filas_salidaM/filas_M, columnas_salidaN/columnas_N
    y_i = (np.arange(filas_salidaM)+ 0.5)/sy_real - 0.5
    x_i = (np.arange(columnas_salidaN) + 0.5)/sx_real -0.5

    y_origen, x_origen = np.floor(y_i).astype(int), np.floor(x_i).astype(int)
    distancia_y = y_i - y_origen
    distancia_x = x_i - x_origen

    
    if interp == "VMC":

        y_vecino = np.where(distancia_y < 0.5, y_origen, y_origen + 1)
        x_vecino = np.where(distancia_x < 0.5, x_origen, x_origen + 1)
        Y = np.clip(y_vecino[:,None], 0, filas_M - 1)
        X = np.clip(x_vecino[None, :], 0, columnas_N - 1)  

        return imagenRGB[Y, X]
    
    elif interp == "Bilineal":

        y_1, x_1 = y_origen + 1, x_origen + 1


        distancia_y, distancia_x = distancia_y[:, None], distancia_x[None, :]
        distancia_y, distancia_x = distancia_y[..., None], distancia_x[..., None]

        y_origen, y_1 = np.clip(y_origen, 0, filas_M - 1), np.clip(y_1, 0, filas_M - 1)
        x_origen, x_1 = np.clip(x_origen, 0, columnas_N - 1), np.clip(x_1, 0, columnas_N -1 )

        f_11 = imagenRGB[y_origen[:, None], x_origen[None, :]]
        f_12 = imagenRGB[y_origen[:, None], x_1[None, :]]
        f_21 = imagenRGB[y_1[:, None], x_origen[None, :]]
        f_22 = imagenRGB[y_1[:, None], x_1[None, :]]
 
        imagen_salida = (1-distancia_y)*(1-distancia_x)*f_11 + (1-distancia_y)*distancia_x*f_12 + distancia_y*(1-distancia_x)*f_21 + distancia_y*distancia_x*f_22
        imagen_salida = np.rint(imagen_salida).astype(imagenRGB.dtype)
        return imagen_salida
    else:
        raise ValueError("Interpolación incorrecta")


''' P4_IMG_2267_CFA.tif '''
''' Bosque.jpeg '''
''' paisaje.jpeg '''
''' PruebaMorado.jpeg '''

s = 1.6
imagen = cv2.imread("Imagenes/ArchivosT1/Bosque.jpeg")
imagenRGB = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
imagen_escalada = Reescalado(imagenRGB, s, "VMC")
plt.imshow(imagen_escalada)
plt.show()