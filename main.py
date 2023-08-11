import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"]="" # 隐藏 pygame 的欢迎信息
import pygame

# 初始化 Pygame
pygame.init()
pygame.display.set_caption('Scratch')

# 创建屏幕和加载图片
width, height = 816, 614.4
screen = pygame.display.set_mode((width, height))
mask_image = pygame.image.load("background.jpg")
image = pygame.image.load("scratch.jpg")

image = pygame.transform.scale(image, (width, height))
mask_image = pygame.transform.scale(mask_image, image.get_size())

mask_surface = mask_image.convert_alpha()
image_surface = image.convert_alpha()

result_surface = pygame.Surface(image.get_size(), flags=pygame.SRCALPHA)

# 设置刮开的阈值
threshold = 0.7

def main():
    global mask_surface
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.circle(mask_surface, (0, 0, 0, 0), event.pos, 40)

            if event.type == pygame.QUIT:
                pygame.quit()
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
        if transparency2 > threshold:
            # 如果达到阈值，清除遮罩
            mask_image = pygame.transform.scale(image, (816, 614.4))
            mask_surface = mask_image.convert_alpha()

        pygame.display.flip()

if __name__ == "__main__":
    main()
