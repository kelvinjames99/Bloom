# -*- coding: utf-8 -*-
import cv2
import numpy

def convert_and_save(img, nome):
    img = img * 255
    cv2.imwrite('{}.jpg'.format(nome), img)            
    
def bloom_gaussian(caminho, limiar, sigma, alfa, beta):
    bright_pass = cv2.imread(caminho)
    for i in range(bright_pass.shape[0]):#brightpass
        for j in range(bright_pass.shape[1]):
            if((0.299*bright_pass[i, j, 2] + 0.587*bright_pass[i, j, 1] + 0.114*bright_pass[i, j, 0]) < limiar):
                bright_pass[i, j, :] = 0
    cv2.imshow('bright-pass', bright_pass)

    for i in range(5): #cria as 5 imagens com o filtro da gaussiana que serão usadas para compor a máscara
        blur = cv2.GaussianBlur(bright_pass, (0, 0), sigma)
        cv2.imwrite('{}.jpg'.format(i), blur)
        sigma = sigma * 2

    mask = cv2.imread('0.jpg').astype('float32')/255        #cria a máscara
    for i in range(4):                      
        aux = cv2.imread('{}.jpg'.format(i+1)).astype('float32')/255
        for x in range(mask.shape[0]):
            for y in range(mask.shape[1]):
                for z in range(mask.shape[2]):
                    if mask[x, y, z] + aux[x, y, z] > 1:
                        mask[x, y, z] = 1
                    else:
                        mask[x, y, z] += aux[x, y, z]

    bloom = cv2.imread(caminho).astype('float32')/255
    for x in range(mask.shape[0]):
        for y in range(mask.shape[1]):
            for z in range(mask.shape[2]):
                bloom[x, y, z] = alfa * bloom[x, y, z] + beta * mask[x, y, z]

    cv2.imshow('mascara', mask)
    convert_and_save(mask, 'mask')
    cv2.imshow('saida', bloom)
    convert_and_save(bloom, 'saida')
  
caminho = './teste.jpg'
cv2.imshow('original', cv2.imread(caminho))
limiar = 150
sigma = 3  
alfa = 1
beta = 0.2
bloom_gaussian(caminho, limiar, sigma, alfa, beta)
cv2.waitKey(0)
cv2.destroyAllWindows()
