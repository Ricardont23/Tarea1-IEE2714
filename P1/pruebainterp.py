import matplotlib.pyplot as plt
import numpy as np

def graficar_puntos_control(puntos_control: np.ndarray):
    
    h = puntos_control[:, 0]
    m = puntos_control[:, 1]
    
    h_ext = np.append(h, h[0] + 360.0)
    m_ext = np.append(m, m[0])
    

    plt.figure(figsize=(10, 5))
    plt.plot(h_ext, m_ext, marker="o", linestyle="-", color="blue", linewidth=2, label="Curva de mapeo m(h)")
    plt.axhline(y=1.0, color="red", linestyle="--", linewidth=1.5, label="Valor neutro (m=1.0)")
    
    plt.title("Mapeo de Saturacion de Color")
    plt.xlabel("Tono (Grados)")
    plt.ylabel("Modificador (m)")
    
    plt.xlim(0, 360)
    plt.xticks(np.arange(0, 361, 30)) 
    
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.legend()
    plt.show()



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

puntos_amarillos_reducido = np.array([ [0.0, 1.0], 
                                        [50.0, 0.3], 
                                        [90.0, 0.6],  
                                        [250.0, 1.0],])

graficar_puntos_control(puntos_amarillos_reducido)
