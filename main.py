import pygame
import pygame_menu
from config import WIDTH , HEIGHT,SIZE,BLACK,WHITE,POSI_INFI,NEGA_INFI
from draught import Game
from AI import minimax,negamax,alpha_beta_pruning
depth = 4   #搜索深度,默认搜索4层
ai_turn = BLACK   #AI棋子的颜色
algorithm = 1     #搜索算法,1为negamax;2为alpha-bate pruning

#选择使用的搜索算法
def select_algorithm(value, index):
    global algorithm
    algorithm = index

#选择自己棋子的颜色
def select_turn(value, index):
    global ai_turn
    if index == 2:
        ai_turn = WHITE
    else:
        ai_turn = BLACK

#设置搜索深度
def set_depth(value):
    global depth
    #如果输入字符串为纯数字，将深度设为该数字；否则使用默认深度
    if value.isdigit():
        value_ = int(value)
        #搜索深度为奇数时，最后一层无意义
        if value_ % 2:
            depth = value_ - 1
        else:
            depth = value_

#运行跳棋ai游戏
def run_game():
    global depth,ai_turn,algorithm
    is_run = True
    #初始化游戏类
    if ai_turn == BLACK:
       game = Game(win,WHITE)
    else:
        game = Game(win,BLACK)
    
    while is_run:
        for event in pygame.event.get():
            #当按Esc时退出游戏
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_run = False 
            
            #判断当前是玩家还是ai的回合
            if game.turn == ai_turn:
                if algorithm == 1:
                    score,new_board = negamax([0],game.board, ai_turn, depth, game)
                else:
                    score,new_board = alpha_beta_pruning([0],game.board, ai_turn,NEGA_INFI , POSI_INFI, depth, game)              
                if new_board:
                    game.ai_move(new_board)
            else:
                game.get_moves()

            
            #判断是否有人获胜
            if game.board.winner() != None:
                game.draw_winner()
                is_run = False
            
            #获取鼠标点击信息，对棋子进行选中和移动
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x , y = pos
                game.after_click(y//SIZE,x//SIZE)
        
        game.update()

pygame.init()
#初始化主窗口
win = pygame.display.set_mode((WIDTH,HEIGHT))
#初始化菜单
menu = pygame_menu.Menu(400,
                        400,
                        'Welcome',
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add_selector('Algorithm :', [('minimax',1), ('a-b pruning',2)],
                  onchange=select_algorithm)
menu.add_selector('My Turn :', [('WHITE',1), ('BLACK',2)],
                  onchange=select_turn)
menu.add_text_input('Depth :', default= 4, onchange=set_depth)#默认深度为4
menu.add_button('Play', run_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(win)



 