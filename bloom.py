# -*- coding: utf-8 -*-
import cv2
import numpy

def convert_and_save(img, nome):
    img = img * 255
    cv2.imwrite('{}.jpg'.format(nome), img)            

def filtro_bright_pass(caminho):
    bright_pass = cv2.imread(caminho)
    for i in range(bright_pass.shape[0]):
        for j in range(bright_pass.shape[1]):
            if((0.299*bright_pass[i, j, 2] + 0.587*bright_pass[i, j, 1] + 0.114*bright_pass[i, j, 0]) < limiar):
                bright_pass[i, j, :] = 0
    cv2.imshow('bright-pass', bright_pass)
    return bright_pass

def bloom_gaussian(caminho, limiar, sigma, alfa, beta):
    bright_pass = filtro_bright_pass(caminho)
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
  
def bloom_boxblur(caminho, janela, alfa, beta):
    bright_pass = filtro_bright_pass(caminho)
    for i in range(5):
        blur = cv2.medianBlur(bright_pass, janela)
        cv2.imwrite('{}b.jpg'.format(i), blur)
        janela = janela * 3 

    mask = cv2.imread('0b.jpg').astype('float32')/255        #cria a máscara
    for i in range(4):                      
        aux = cv2.imread('{}b.jpg'.format(i+1)).astype('float32')/255
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
    cv2.imshow('saidaB', bloom)
    convert_and_save(bloom, 'saidaB')

caminho = './cross.jpg'
cv2.imshow('original', cv2.imread(caminho))
limiar = 150
sigma = 3  
alfa = 1
beta = 0.2
bloom_gaussian(caminho, limiar, sigma, alfa, beta)
bloom_boxblur(caminho, 3, alfa, beta)
cv2.waitKey(0)
cv2.destroyAllWindows()