from PIL import Image
import pytesseract
import cv2
import numpy as np
from collections import deque
from matplotlib import pyplot as plt

# Faz uma matriz circular em relacao a um filtro de tamanho n
def wrap(img, n):
    m = n//2
    ret = np.zeros((img.shape[0] + 2*m, img.shape[1] + 2*m))

    for i in range(img.shape[0] + 2*m):
        for j in range(img.shape[1] + 2*m):
            ii = (i - m)%img.shape[0]
            jj = (j - m)%img.shape[1]
            ret[i, j] = img[ii, jj]

    return ret

# Implementacao do Filtro Adaptativo de Reducao do Ruido Local
# Iout = Inoisy - (var_noisy/var_N)*(Inoisy - MeanN)
def filtro_adaptativo_reducao(img, n, alpha, EPS = 0.001):
    ret = np.zeros(img.shape).astype(np.float)
    img = wrap(img, n).astype(np.float)

    var = alpha*alpha
    m = n//2

    for i in range(ret.shape[0]):
        for j in range(ret.shape[1]):
            # pixel de img estao deslocados em relacao a sua posicao original devido ao wrap
            ii = i + m
            jj = j + m

            filtro = img[ii-m:ii+m+1, jj-m:jj+m+1]

            # Calculo da media
            media = np.mean(filtro)
            # Calculo da variacao local
            var_local = np.var(filtro)

            # Se var_local muito pequena mantem pixel
            if(var_local < EPS):
                ret[i,j] = img[ii,jj]
            else:
                # aplicacao da formula
                ret[i,j] = img[ii,jj] - (var*(img[ii,jj] - media))/var_local

    return ret.astype(np.uint8)

# Implementacao do Filtro Adaptativo de Mediana
def filtro_adaptativo_mediana(img, n, M):
    ret = np.zeros(img.shape).astype(np.float)
    img = wrap(img, M).astype(np.float)

    for i in range(ret.shape[0]):
        for j in range(ret.shape[1]):
            # pixel de img estao deslocados em relacao a sua posicao original devido ao wrap
            ii = i + M//2
            jj = j + M//2

            # Etapa A
            while(n <= M):
                m = n//2

                if(n%2 == 1):
                    # se filtro impar deslocamento normal
                    filtro = img[ii-m:ii+m+1, jj-m:jj+m+1]
                else:
                    # se filtro par deslocamento normal o centro é o pixel da esquerda dentre os 2 empatados
                    filtro = img[ii-m+1:ii+m+1, jj-m+1:jj+m+1]

                zmed = np.median(filtro)    # calculo da mediana
                zmin = np.amin(filtro)      # calculo do minimo
                zmax = np.amax(filtro)      # calculo do maximo

                a1 = zmed - zmin
                a2 = zmed - zmax

                if(a1 > 0 and a2 < 0):
                    # Etapa B
                    b1 = img[ii, jj] - zmin
                    b2 = zmed - zmax
                    if(b1 > 0 and b2 < 0):
                        ret[i,j] = img[ii,jj]
                    else:
                        ret[i,j] = zmed
                    break
                else:
                    n+=1
                    if(n > M):
                        ret[i,j] = zmed
    

    return ret.astype(np.uint8)

# Implementacao do Filtro Adaptativo de Reducao do Ruido Local
# Iout = sum(g**(Q+1)) / sum(g**Q)
# g eh a regiao de Inoisy delimitada pelo filtro centrado em x,y
def filtro_media_contra_harmonica(img, n, Q):
    ret = np.zeros(img.shape).astype(np.float)

    m = n//2

    for i in range(ret.shape[0]):
        for j in range(ret.shape[1]):
            # preenchimento pelo valor zero em todas as posicoes fora da imagem
            i1 = max(i-m, 0)
            i2 = min(i+m+1, ret.shape[0])

            j1 = max(j-m, 0)
            j2 = min(j+m+1, ret.shape[1])

            filtro = img[i1:i2, j1:j2]

            # evitar divisao por zero
            if (Q < 0 and np.amin(filtro) == 0):
                ret[i,j] = img[i,j]
            else:
                # calculo da formula
                A = np.sum(np.power(filtro, Q + 1))
                B = np.sum(np.power(filtro, Q))
                ret[i,j] = A/B


    return ret.astype(np.uint8)

# Retorna o histograma dos pixels de uma imagem
def histogram (image) :
	h = np.zeros((256), dtype=int);
	for x in range(0, image.shape[0]) :
		for y in range(0, image.shape[1]) :
			h[image[x, y]] = h[image[x, y]] + 1
	return h

# Equalização de uma imagem(image) dado um histograma acumulado (h) e 
# o valor máximo do pixel(pixels)
def equalization (image, h, pixels) :
	n, m = image.shape
	new_image = np.zeros((n, m), dtype=np.uint8)
	for x in range(0, n) :
		for y in range(0, m) :
			new_image[x, y] = ((h[image[x, y]] * 255.) / float(pixels)).astype(np.uint8)
	return new_image
	
# Equalização de uma imagem
def individualTransference (image) :
	h = histogram(image)    # Calculo do histograma

    # Histograma acumulado
	for x in range(1, 256) :
		h[x] += h[x-1] 
	
    # Equalização
	return equalization(image, h, image.shape[0] * image.shape[1])

def erode (image, kernel, iterations) :
	new_image = np.ones(image.shape)
	n, m = image.shape
	dx, dy = kernel.shape
	dx = int(dx / 2)
	dy = int(dy / 2)
	sub_mat = np.zeros(kernel.shape)
	print(dx)
	print(dy)
	for it in range(iterations) :
		new_image = image
		for x in range(dx, n - dx) :
			for y in range(dy, m - dy) :
				sub_mat = image[x - dx : x + dx+1, y - dy : y + dy+1]
				if (np.max(sub_mat) < 255) :
					new_image[x, y] = 0
		image = new_image
		print(it)
	
	return image
filename = str(input()).strip()
img = cv2.imread("images/" + filename)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray_img = cv2.fastNlMeansDenoising(gray_img, None, 3, 11, 33)
gray_img = cv2.resize(gray_img, None, fx=11, fy=11, interpolation = cv2.INTER_CUBIC)
kernel = np.ones((2,2), np.uint8)
gray_img = cv2.erode(gray_img, kernel, iterations=3)

cv2.imwrite("output_image/" + filename, gray_img)
print( pytesseract.image_to_string( gray_img ) ) # Extraindo o texto da imagem

