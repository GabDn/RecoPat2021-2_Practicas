import matplotlib.pyplot as plt
import cv2
import skimage as ski
import PIL as pil
import imageio as io
import numpy as np
from PIL import Image, ImageFilter
from shapely.geometry import Polygon, MultiPolygon
from descartes import PolygonPatch

# Esta funcion 'desdobla' cadenas para crear un rango y un numero
# eg: '100'=mayores que 100, '0-50'= entre 0 y 50, '10-20,500'= entre 10 y 20 o mayores de 500
def listRanger(rango: str):
    # Separa la cadena por comas
    rango = rango.split(',')
    # Definicion de las variables de retorno
    listarango = []
    mayorq = -1
    # Recorre las sentencias separadas anteriormente
    for x in rango:
        # Si la sentencia tiene un '-' es un rango
        if '-' in x:
            # Los rangos se añaden a la lista listarango
            listax = x.split('-')
            listarango += list(range(int(listax[0]),int(listax[1])))
        # Si no, es una cota inferior
        else:
            # Solo puede existir una de estas cotas en la sentencia
            mayorq = int(x)

    return [listarango, mayorq]

# Esta función imprime la imagen junto con las curvas de la posición nColl de contornos
# Que cumplan con range y retorna un arreglo con dichas curvas.
# Se puede especificar los puntos en el perimetro de las lineas con range. eg: range='400-560'
# Si no se especifica se utiliza '150'
# Se puede especificar un nombre para guardar la imagen resultante con save. eg: save='imagen2.png'
# Si no se especifica se utiliza 'ImCrTMP.png'
# eg: masker.printImCr(fruta, fruta_contornos, 1, range='200', save='comida_contornos.png')
def printImCr(imagen, contornos, nColl, **kwargs):
    # Desdobla range
    rangolstd = listRanger(kwargs["range"] if ("range" in kwargs) else '150')
    # Define variable de retorno
    curvas_array = []
    # Con este for se muestran todas las lineas cuya primera dimension entre en el rango
    for i in contornos.collections[nColl].get_paths():
        # Si cumple con las caracteristicas indicadas en range se añade al plot y a la var de retorno
        if len(i.vertices) in rangolstd[0] or ((len(i.vertices) > rangolstd[1]) if (rangolstd[1] != -1) else (len(i.vertices) > len(i.vertices)+1)):
            plt.plot(i.vertices[:,0], i.vertices[:,1], '--b')
            curvas_array.append(i.vertices)
    # Muestra la imagen
    plt.imshow(imagen)
    plt.axis('off')
    # Salva la imagen
    plt.savefig('resultados/'+kwargs["save"] if ("save" in kwargs) else 'resultados/ImCrTMP.png', bbox_inches='tight', transparent=False, pad_inches = 0)
    # Regresa el arreglo
    return curvas_array

# Esta función imprime la imagen de fondo junto con los poligonos
# Definidos por las curvas en curvas_arr
# Retorna un obj Multipolygon
def printImPoly(curvas_arr, fondo):
    # Arreglo aux
    poly_array = []
    # Recorre arreglo de curvas
    for crvua in curvas_arr:
        x = crvua[:,0]
        y = crvua[:,1]
        poly_array.append(Polygon([(i[0], i[1]) for i in zip(x,y)]))
    polygons = MultiPolygon(poly_array)
    #len(polygons.geoms)
    #polygons
    fig = plt.figure() 
    ax = fig.gca()

    # Plotea la imagen de fondo
    plt.imshow(fondo)
    # Plotea los poligonos
    for poly in polygons:
        ax.add_patch(PolygonPatch(poly))
    #ax.axis('scaled')
    plt.show()
    # Retorna los poligonos
    return polygons

def listaPlatanos():
    platanos1 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento1-platanos.jpg'))
    platanos2 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento2-platanos.jpg'))
    platanos3 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento3-platanos.jpg'))
    platanos4 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento4-platanos.jpg'))
    return [platanos1,platanos2,platanos3,platanos4]
def listaChiles():
    chiles1 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento1-chiles.jpg'))
    chiles2 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento2-chiles.jpg'))
    chiles3 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento3-chiles.jpg'))
    chiles4 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento4-chiles.jpg'))
    return [chiles1,chiles2,chiles3,chiles4]
def listaHuevos():
    huevos1 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento1-huevos.jpg'))
    huevos2 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento2-huevos.jpg'))
    huevos3 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento3-huevos.jpg'))
    huevos4 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento4-huevos.jpg'))
    return [huevos1,huevos2,huevos3,huevos4]
def listaFondos():
    fondos1 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento1-fondos.jpg'))
    fondos2 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento2-fondos.jpg'))
    fondos3 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento3-fondos.jpg'))
    fondos4 = np.array(io.imread('comida-entrenamiento-procesado/Entrenamiento4-fondos.jpg'))
    return [fondos1,fondos2,fondos3,fondos4]

def pixelsMatrix(clase):
    lista_comida = globals()["lista"+clase]()
    #lista_comida = getattr(self, "lista"+clase)()
    pixeles_comida = []
    for platano in lista_comida:
        for renglon in platano:
            for pixel in renglon:
                if pixel.mean() > 0.:
                    pixeles_comida.append(pixel)
    return np.array(pixeles_comida)