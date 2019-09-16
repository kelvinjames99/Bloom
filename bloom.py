# -*- coding: utf-8 -*-
import cv2
import numpy

def convert_and_save(img):

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for z in range(img.shape[2]):
                img[i, j, z] = img[i, j, z] * 255 


caminho = './chronocross.jpg'
img = cv2.imread(caminho)
limiar = 150
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if((0.299*img[i, j, 2] + 0.587*img[i, j, 1] + 0.114*img[i, j, 0]) < limiar):
            img[i, j, :] = 0
sigma = 3
   
for i in range(5):
    blur = cv2.GaussianBlur(img, (0, 0), sigma)
    cv2.imwrite('{}.jpg'.format(i), blur)
    sigma = sigma * 2

mask = cv2.imread('0.jpg').astype('float32')/255
for i in range(4):
    aux = cv2.imread('{}.jpg'.format(i+1)).astype('float32')/255
    #cv2.imshow('{}'.format(i+1), aux)
    for x in range(mask.shape[0]):
        for y in range(mask.shape[1]):
            for z in range(mask.shape[2]):
                if mask[x, y, z] + aux[x, y, z] > 1:
                    mask[x, y, z] = 1
                else:
                    mask[x, y, z] += aux[x, y, z]


alfa = 1
beta = 0.2
imagem = cv2.imread(caminho).astype('float32')/255
for x in range(mask.shape[0]):
    for y in range(mask.shape[1]):
        for z in range(mask.shape[2]):
            imagem[x, y, z] = alfa * imagem[x, y, z] + beta * mask[x, y, z]

cv2.imshow('mascara', mask)
convert_and_save(mask)
cv2.imwrite('mask.jpg', mask)
cv2.imshow('saida', imagem)
convert_and_save(imagem)    
cv2.imwrite('result.jpg', imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
