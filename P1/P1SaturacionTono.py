import matplotlib.pyplot as plt
import cv2
import numpy as np
import skimage

def creacion_malla (puntos_control: np.ndarray, hue: np.ndarray):

    M = np.zeros_like(hue)

    hue_mod = np.where(hue < puntos_control[0][0], hue + 360.0, hue)

    for i in range( len(puntos_control) ):
        x1, y1 = puntos_control[i]
        try:
            x2, y2 = puntos_control[i+1]
        except IndexError:
            x2, y2 = puntos_control[0][0] + 360.0 , puntos_control[0][1]

        malla_hue = hue_mod[(hue_mod >= x1) & (hue_mod < x2)]

        pendiente = (y2-y1)/(x2-x1)

        M[(hue_mod >= x1) & (hue_mod < x2) ] = y1 + pendiente*(malla_hue - x1)

    return M

def rgb_a_hsi(imagen: np.ndarray):

    imagen = imagen.astype(np.float64)
    imagen = imagen/ 255.0

    R = imagen[:, :, 0]
    G = imagen[:, :, 1]
    B = imagen[:, :, 2]

    epsilon = 1e-10

    I = (R + G + B) / 3.0

    rgb_minimo = np.minimum(np.minimum(R, G), B)
    rgb_maximo = np.maximum(np.maximum(R, G), B)
    delta = rgb_maximo - rgb_minimo
    S = 1.0 - (3.0 / (R + G + B + epsilon)) * rgb_minimo

    theta = np.arccos(np.clip(( 0.5 * ((R - G) + (R - B)) ) / ( np.sqrt((R -G) ** 2 + (R - B) * (G - B)) + epsilon ), -1.0, 1.0))

    H = np.degrees(theta)
    H = np.where(B > G, 360.0 - H, H)

    H = np.where(delta < epsilon, 0.0, H)

    imagen_HSI = np.stack([H, S, I], axis=-1)
    return imagen_HSI

def rgb_a_cielch(imagen: np.ndarray):

    imagen = imagen.astype(np.float64)
    imagen = imagen/255.0
    imagen_lab =  skimage.color.rgb2lab(imagen)
    imagen_lch = skimage.color.lab2lch(imagen_lab)

    return imagen_lch

def deconversion_lch(imagen: np.ndarray):

    imagen_lab = skimage.color.lch2lab(imagen)
    imagen_rgb = skimage.color.lab2rgb(imagen_lab)

    return imagen_rgb

def deconversion_hsi(imagen_hsi: np.ndarray):   

    H = imagen_hsi[:, :, 0] % 360
    S = np.clip(imagen_hsi[:, :, 1], 0.0, 1.0)
    I = np.clip(imagen_hsi[:, :, 2], 0.0, 1.0)

    epsilon = 1e-10
    Hr = np.radians(H)

    R = np.zeros_like(I)
    G = np.zeros_like(I)
    B = np.zeros_like(I)

    # Sector RG: 0 <= H < 120
    malla = (H >= 0) & (H < 120)

    B[malla] = I[malla] * (1 - S[malla])
    R[malla] = I[malla] * (1 + (S[malla] * np.cos(Hr[malla])) / (np.cos(np.radians(60) - Hr[malla]) + epsilon))
    G[malla] = 3 * I[malla] - (R[malla] + B[malla])

    # Sector GB: 120 <= H < 240
    malla = (H >= 120) & (H < 240)

    Hp = Hr[malla] - np.radians(120)

    R[malla] = I[malla] * (1 - S[malla])
    G[malla] = I[malla] * (1 + (S[malla] * np.cos(Hp)) / (np.cos(np.radians(60) - Hp) + epsilon))
    B[malla] = 3 * I[malla] - (R[malla] + G[malla])

    # Sector BR: 240 <= H <= 360
    malla = (H >= 240) & (H <= 360)

    Hp = Hr[malla] - np.radians(240)

    
    G[malla] = I[malla] * (1 - S[malla])
    B[malla] = I[malla] * (1 + (S[malla] * np.cos(Hp)) / (np.cos(np.radians(60) - Hp) + epsilon))
    R[malla] = 3 * I[malla] - (G[malla] + B[malla])

    imagen_rgb = np.clip(np.stack([R, G, B], axis=-1), 0.0, 1.0)
    return imagen_rgb

def ColorSaturation(imagen: np.ndarray, puntos: np.ndarray, espacio_color: str):

    if espacio_color == "HSI":

        imagen_hsi = rgb_a_hsi(imagen)
        H = imagen_hsi[:, :, 0]
        S = imagen_hsi[:, :, 1]
        M = creacion_malla (puntos, H)

        #funcion g_m(h):
        S[:] = np.clip(S * M, 0.0, 1.0) 

        #devolver la imagen a rgb y retornar:
        imagen_rgb = deconversion_hsi(imagen_hsi)
        return imagen_rgb
    
    elif espacio_color == "LCH":

        imagen_lch = rgb_a_cielch(imagen)
        Hr = imagen_lch[:, :, 2]
        H = np.degrees(Hr)
        C = imagen_lch[:, :, 1]
        M = creacion_malla(puntos, H)

        C[:] = np.clip(C * M, 0.0, None) 

        imagen_rgb = deconversion_lch(imagen_lch)
        imagen_rgb = np.clip(imagen_rgb, 0.0, 1.0)
        return imagen_rgb
    else:
        raise ValueError("Espacio no compatible")


#Amplificación mayoritaria [100-250]; Atenuacion [350-40]
#En HSI: Amplificación de tonos Azules, Celestes y Verdes, Atenuación de Tonos Rojos
#En LCH: Amplificacion Amarillos, Verdes y Celestes, Atenuacion de Rojos y Magentas
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

#Amplificación de [260-65]
#En HSI: Amplificación de Tonos Morados, Rojos y Amarillos
#En LCH: Amplificación de Tonos Azules, Morados, Rojos y Naranjos
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


#Atenuación [25-100]
#En HSI: Atenuación de tonos Naranjos, Amarillos y Verdes Claros
#En LCH: Antenuación de tonos Rojos, Naranjos, Amarillos y Verdes Claros
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

puntos_amarillos_reducido = np.array([ [0.0, 1.0], 
                                        [50.0, 0.3], 
                                        [90.0, 0.6],  
                                        [250.0, 1.0],])

puntos_neutro = np.array([ [0.0, 1.0], 
                            [50.0, 1.0], 
                            [90.0, 1.0],  
                            [250.0, 1.0],])


''' P1_IMG_2402.tif '''
''' PruebaTonos.jfif '''




imagen = cv2.imread("Imagenes/ArchivosT1/PruebaTonos.jfif ")
imagenRGB = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
imagen_saturada = ColorSaturation(imagenRGB, puntos_azules, "HSI")
plt.imshow(imagen_saturada)
plt.show()




