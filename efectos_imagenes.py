import cv2
import numpy as np
import math

#la funcion hue recibe la copia de la imagen original y el angulo dado en la entrada para aplicarselo a la imagen y devolverla con el tinte modificado
def hue(nuevaImagen,angulo):
    x = convertir_rgb_hsv(nuevaImagen)
    height = len(nuevaImagen)
    width = len(nuevaImagen[0])
    bands = len(nuevaImagen[0][0])
    for i in range(0,height):
        for j in range(0,width):
            x[i][j][0]+=angulo
            if x[i][j][0] > 360:
                x[i][j][0] -= 360
    return convertir_hsv_rgb(x)
#la funcion sat recibe la copia de la imagen original y la proporcion dada en la entrada para aplicarselo a la imagen y devolverla con la saturacion modificada
def sat(nuevaImagen,proporcion):
    x = convertir_rgb_hsv(nuevaImagen)
    height = len(nuevaImagen)
    width = len(nuevaImagen[0])
    bands = len(nuevaImagen[0][0])
    for i in range(0,height):
        for j in range(0,width):
            x[i][j][1]*=proporcion
    return convertir_hsv_rgb(x)

#la funcion val recibe la copia de la imagen original y la proporcion dada en la entrada para aplicarselo a la imagen y devolverla con el brillo modificado
def val(nuevaImagen,proporcion):
    x = convertir_rgb_hsv(nuevaImagen)
    height = len(nuevaImagen)
    width = len(nuevaImagen[0])
    bands = len(nuevaImagen[0][0])
    for i in range(0,height):
        for j in range(0,width):
            x[i][j][2]*=proporcion
    return convertir_hsv_rgb(x)

#funcion_desenfoque recibe posiciones (x,y) y la desviacion para crear la formula de la matriz de convolucion
def funcion_desenfoque(x,y,des):
    funcion =(1/(2*math.pi*des**2))*math.e**(-((x**2+y**2)/(2*des**2)))
    return funcion
#recibe el kernel y la desviacion estandar y crea la matriz de convolucion
def matriz_convolucion(ker,desv):
    n=(ker*2)+1
    matriz_con=np.zeros((n,n))
    c = n//2
    for i in range (n):
        for k in range(n):
            x=abs(i-c)
            y=abs(k-c)
            matriz_con[i][k]=funcion_desenfoque(x,y,desv)
            lista = [matriz_con,n]
    print(matriz_con)
    return lista
#recibe el kernel y la desviacion estandar y la matriz de convolucion, esta ultima la aplica a la copia de la imagen y retorna la imagen con efecto gaussiano
def blur (Imagen_desenfoque,ker,desv):
    lista = matriz_convolucion(ker,desv)
    matriz_con = lista[0]
    n = lista[1]
    height = len(Imagen_desenfoque)
    width = len(Imagen_desenfoque[0])
    bands = len(Imagen_desenfoque[0][0])
    imagenblur = np.zeros([height,width,bands],dtype=np.uint8)
    suma=0
    for i in range (n):
        for j in range (n):
            suma +=matriz_con[i][j]
    for i in range (n):
        for j in range (n):
            matriz_con[i][j]=matriz_con[i][j]/suma
            
    for i in range (height):
        for j in range (width):
            acum=0
            for k in range (n):
                for l in range (n):
                    Ipri=i-ker+k
                    Jpri=j-ker+l
                    if Ipri>=0 and Ipri<height and Jpri>=0 and Jpri<width:
                        acum += (Imagen_desenfoque[Ipri][Jpri]*matriz_con[k][l])
            imagenblur[i][j] = acum
            
    return imagenblur

 
#recibe la copia de la imagen y lo que hace es cambiar la imagen de rgb a hsv
def convertir_rgb_hsv(nuevaImagen):
    height = len(nuevaImagen)
    width = len(nuevaImagen[0])
    bands = len(nuevaImagen[0][0])
    imagenhsv = np.zeros([height,width,bands])
    for i in range(0,height):
        for j in range(0,width):
            rp = nuevaImagen[i][j][2]/255.0
            gp = nuevaImagen[i][j][1]/255.0
            bp = nuevaImagen[i][j][0]/255.0
            cmax = max(rp,gp,bp)
            cmin = min(rp,gp,bp)
            df = cmax-cmin
            if cmax == cmin:
                H = 0
            elif cmax == rp:
                H = ((60*(gp-bp)/df)+360)%360
            elif cmax == gp:
                H = (((60)*((bp-rp)/df))+120)%360
            elif cmax == bp:
                H = (((60)*(((rp-gp)/df)))+240)%360
            if cmax == 0:
                S = 0
            else:
                
                S = df/cmax
            V = cmax
            imagenhsv[i][j][0]=H
            imagenhsv[i][j][1]=S
            imagenhsv[i][j][2]=V
       
    return imagenhsv

        

# recibe la imagen en formato hsv y la retorna de nuevo en rgb
def convertir_hsv_rgb(imagenhsv):
    height = len(imagenhsv)
    width = len(imagenhsv[0])
    bands = len(imagenhsv[0][0])
    imagenrgb = np.zeros([height,width,bands],dtype=np.uint8)
    for i in range(0,height):
        for j in range(0,width):
            H = imagenhsv[i][j][0]
            S = imagenhsv[i][j][1]
            V = imagenhsv[i][j][2]
            C = V * S
            X = C * (1-abs((H/60%2)-1))
            m = V - C
            if (0)<=H<(60):
                rp = C
                gp = X
                bp = 0
            elif (60)<=H<(120):
                rp = X
                gp = C
                bp = 0
            elif (120)<=H<(180):
                rp = 0
                gp = C                    
                bp = X
            elif (180)<=H<(240):
                rp = 0
                gp = X
                bp = C
            elif (240)<=H<(300):
                rp = X
                gp = 0
                bp = C
            elif(300)<=H<(360):
                rp = C
                gp = 0
                bp = X
                
            r=(rp+m)*255
            g=(gp+m)*255
            b=(bp+m)*255
            if r>255:
                r = 255
            if g>255:
                g = 255
            if b>255:
                b = 255

            imagenrgb[i][j][2]=r
            imagenrgb[i][j][1]=g
            imagenrgb[i][j][0]=b
            
    return imagenrgb

#main lo que hace es ver la entrada y depende de ella retorna las diferentes funciones explicadas anteriormente
def main():
    linea = input().split(" ")
    operacion = linea[1]
   
    image = cv2.imread(linea[0])
    cv2.imshow("image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    height = len(image)
    width = len(image[0])
    bands = len(image[0][0])
    nuevaImagen = np.zeros([height,width,bands])
    for i in range(height):
        for j in range(width):
            for b in range(bands):
                nuevaImagen[i][j][b] = image[i][j][b]

    Imagen_desenfoque = np.zeros([height,width,bands],dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            for b in range(bands):
                Imagen_desenfoque[i][j][b] = image[i][j][b]
    if operacion == "hue":
        n = int(linea[2])
        h = hue(nuevaImagen,n)
        cv2.imshow("hue.jpg",h)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("Copia_hue.jpg",h)
    elif operacion == "sat":
        n = float(linea[2])
        s = sat(nuevaImagen,n)
        cv2.imshow("sat.jpg",s)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("Copia_sat.jpg",s)
    elif operacion == "val":
        n = float(linea[2])
        v = val(nuevaImagen,n)
        cv2.imshow("val.jpg",v)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("Copia_val.jpg",v)
    elif operacion == "blur":
        n = int(linea[2])
        n1 = int(linea[3])
        b = blur(Imagen_desenfoque,n,n1)
        cv2.imshow("blur.jpg",b)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("Copia_blur.jpg",b)
        
        

main()
            
    
                
            
    
    
