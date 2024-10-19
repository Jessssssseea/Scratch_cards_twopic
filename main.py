import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"]="" # 隐藏 pygame 的欢迎信息

import pygame
from win32.win32api import GetSystemMetrics
from PIL import Image
import ctypes
import sys
from tkinter import messagebox

# 初始化 Pygame
pygame.init()
pygame.display.set_caption('刮刮乐')

# 获取图像尺寸
img = Image.open('background.png')
imgSize = img.size
w = img.width
h = img.height

# 获取屏幕分辨率
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# 计算缩放比例
scale_width = screen_width / w
scale_height = screen_height / h
scale = min(scale_width, scale_height)

# 计算缩放后的图像尺寸
width = float(w * scale * 0.75)
height = float(h * scale * 0.75)

screen = pygame.display.set_mode((width, height))
mask_image = pygame.image.load("scratch.png")
image = pygame.image.load("background.png")

image = pygame.transform.scale(image, (width, height))
mask_image = pygame.transform.scale(mask_image, (width, height))

mask_surface = mask_image.convert_alpha()
image_surface = image.convert_alpha()

result_surface = pygame.Surface(image.get_size(), flags=pygame.SRCALPHA)

# 设置刮开的阈值
threshold = 0.7

def main():
    global mask_surface, width, height, threshold, image_surface

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.circle(mask_surface, (0, 0, 0, 0), event.pos, 40)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return

        draw_surface = pygame.Surface(image.get_size(), flags=pygame.SRCALPHA)
        draw_surface.blit(image_surface, (0, 0))
        draw_surface.blit(mask_surface, (0, 0))

        result_surface.fill((255, 255, 255, 255))
        result_surface.blit(draw_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        screen.blit(result_surface, (0, 0))

        # 判断是否达到刮开的阈值
        transparent_pixels = pygame.mask.from_surface(mask_surface).count()
        total_pixels = width * height
        transparency = transparent_pixels / total_pixels
        transparency2 = 1 - transparency

        if transparency2 > threshold:   # 如果达到阈值，清除遮罩
            mask_image = pygame.transform.scale(image, (width, height))
            mask_surface = mask_image.convert_alpha()

        pygame.display.flip()

if __name__ == "__main__":
    main()
