# -*- coding: utf-8 -*-
#将图片转换为点阵图
import cv2
import numpy as np
import tkinter
from PIL import Image, ImageDraw, ImageFont
import abc


# 抽象类
class abstractDraw(metaclass=abc.ABCMeta):
    def __init__(self, img_path):
        self.get_image(img_path)

    def get_image(self, img_path):
        self.img = cv2.imread(img_path)

    @abc.abstractmethod
    def draw(self, output):
        pass

    def resize(self, img_shape):
        self.img = cv2.resize(self.img, img_shape)
        
    def get_gray_img(self):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)

# 将图像转换为彩色文字
class charDraw(abstractDraw):
    txt = '彩色文字'

    def draw(self, output):
        font_size = 10
        font = ImageFont.truetype('simsun.ttc',font_size)
        image = Image.new('RGB', (self.img.shape[1], self.img.shape[0]), (20,20,20))
        d = ImageDraw.Draw(image)
        length = len(self.txt)
        txt_copy = self.txt
        #与字体大小一致
        for i in range(0, self.img.shape[0], font_size):
            for j in range(0, self.img.shape[1], font_size * length):
                for k in range(length):
                    if j+k*font_size >= self.img.shape[1]:
                        continue
                    b = self.img[i][j+k*font_size][0]
                    g = self.img[i][j+k*font_size][1]
                    r = self.img[i][j+k*font_size][2]
                    d.text((j+k*font_size, i), self.txt[k], fill=(r,g,b),font=font)
                    d.text((j+k*font_size, i), self.txt[k], fill=(r,g,b),font=font) #写两遍亮很多
            self.txt = self.txt[length - 1] + self.txt[0: length - 1]
        image.save(output)
    
    
# 将图像转换为黑色气泡
class circleDraw(abstractDraw):
    point_2r = 8
    
    def __init__(self, img_path):
        self.get_image(img_path)
        self.resize((int(self.img.shape[1] / 4), int(self.img.shape[0] / 4)))
        self.get_gray_img()
        self.bg_shape = [self.img.shape[1] * 9, self.img.shape[0] * 9]
    
    def reverse_transfer(self, ratio = 120):
        reserve_img = cv2.bitwise_not(self.img)
        self.arr = reserve_img / ratio
        
    def draw(self, output):
        self.reverse_transfer()
        
        image = Image.new('RGB', self.bg_shape, "white")
        d = ImageDraw.Draw(image)
        init_x = 10
        init_y = 10
        for i in range(self.arr.shape[0]):
            for j in range(self.arr.shape[1]):
                if self.arr[i][j] > 0.1 and (i + j) % 2 == 0:
                    d.ellipse((init_x + j * self.point_2r, init_y + i * self.point_2r, init_x + j * self.point_2r + int(self.point_2r * self.arr[i][j]) ,init_y + i * self.point_2r + int(self.point_2r * self.arr[i][j])),fill = 'black', outline ='black')
        image.save(output)

# 将图像转换为符号
class signDraw(abstractDraw):
    ascii_list = list(r"$@&%A#=-.^!~ ")
    point_2r = 8
    
    def __init__(self, img_path):
        self.get_image(img_path)
        self.resize((int(self.img.shape[1] / 5), int(self.img.shape[0] / 5)))
        self.get_gray_img()
        self.bg_shape = [self.img.shape[1] * 8, self.img.shape[0] * 8]
    
    def reverse_transfer(self, ratio = 20):
        reserve_img = cv2.bitwise_not(self.img)
        self.arr = reserve_img / ratio

    def draw(self, output):
        self.reverse_transfer()
    
        image = Image.new('RGB', self.bg_shape, "black")
        d = ImageDraw.Draw(image)
        init_x = 10
        init_y = 10
        for i in range(self.arr.shape[0]):
            for j in range(self.arr.shape[1]):
                if self.arr[i][j] > 0.1:
                    d.text((init_x + j * self.point_2r, init_y + i * self.point_2r), self.ascii_list[int(self.arr[i][j])], (255,255,255))
        image.save(output)


class drawFactory:
    def __init__(self, method, img_path):
        if method == 'char':
            self.drawObj = charDraw(img_path)
        elif method == 'circle':
            self.drawObj = circleDraw(img_path)
        elif method == 'sign':
            self.drawObj = signDraw(img_path)
    
    def draw(self, output = './output.jpg'):
        self.drawObj.draw(output)
    
    
if __name__ == '__main__':
    d = drawFactory('circle', 'the-look.jpg')
    d.draw()
