# -*- coding:utf-8 -*-
import pygame
import crown

#正负无穷
POSI_INFI = 2147483647
NEGA_INFI  = -2147483647

#颜色
WHITE = (255,255,255)
BLUE = (0,0,255)
BLACK = (0,0,0)
GREY1 = (209,203,180)
GREY2 = (194,194,194)
GREEN = (114,139,114)

#棋盘信息
WIDTH , HEIGHT = 640 , 680  #界面的宽高
ROWS , COLS = 8 , 8         #棋盘的行列数
SIZE = 80                   #棋格宽度

#皇冠图片
WHITE_CROWN = pygame.transform.scale(pygame.image.load('crown/white.jpg'), (44, 25))
BLACK_CROWN = pygame.transform.scale(pygame.image.load('crown/black.jpg'), (44, 25))



