import pygame
from copy import deepcopy
from config import WHITE,BLACK,POSI_INFI,NEGA_INFI

def minimax(path_num,current_board,color,depth,game):
    if depth == 0 or current_board.winner():
        return current_board.evaluate(game.my_turn),current_board
    
    best_move = None
    #颜色转换
    if color == WHITE:
        other_color = BLACK
    else:
        other_color = WHITE
    if color != game.my_turn:
        max_score = NEGA_INFI
        for move in get_all_moves(path_num,current_board,color,game):
            score = minimax(path_num,move,other_color, depth - 1, game)[0]
            max_score = max(score,max_score)
            if max_score == score:
                best_move = move
        return max_score , best_move
    else:
        min_score = POSI_INFI
        for move in get_all_moves(path_num,current_board,color,game):
            score = minimax(path_num,move,other_color, depth - 1, game)[0]
            min_score = min(score,min_score)
            if min_score == score:
                best_move = move
        return min_score , best_move

def negamax(path_num,current_board,color,depth,game):
    '''
      negamax(负极值算法)是对 minimax（极大极小算法）做出的小改进
      通过max(a,b) = - min(-a,-b)思想将极大、极小情况统一，精简代码量
    '''
    #当深度为0或者已经搜索除有一方获胜，没有继续搜索的必要，返回
    if depth == 0 or current_board.winner() != None:
        return current_board.evaluate(game.my_turn),current_board
    
    best_move = None
    best = NEGA_INFI
    #颜色转换
    if color == WHITE:
        other_color = BLACK
    else:
        other_color = WHITE
    for move in get_all_moves(path_num,current_board,color,game):
        score = -negamax(path_num,move,other_color,depth - 1,game)[0]
        #选择最优解
        best = max(score,best)
        if best == score:
            best_move = move

    return best , best_move

def alpha_beta_pruning(path_num,current_board,color,alpha,beta,depth,game):
    '''
     基于nagamax的 alpha-beta剪枝
    '''
    #当深度为0或者已经搜索出有一方获胜，没有继续搜索的必要，返回
    if depth == 0 or current_board.winner() != None:
        return current_board.evaluate(game.my_turn),current_board  
    #颜色转换
    if color == WHITE:
        other_color = BLACK
    else:
        other_color = WHITE
    best_move = None
    moves = get_all_moves(path_num,current_board,color,game)
    if moves:
        for move in moves:
            score = -alpha_beta_pruning(path_num,move,other_color,-beta,-alpha,depth - 1,game)[0]
            if score >= beta:
                return beta,best_move
            if score > alpha:
                alpha = score
                best_move = move
        return alpha,best_move
    else:#无可移动的路径时返回负无穷
        return 1+NEGA_INFI,best_move

#模拟移动
def simulate_move(piece, move, board,  skip):
    '''
     模拟棋盘棋子的移动，返回移动后的新棋盘
    '''
    board.move_piece(piece, move[0], move[1])
    if skip:
        board.remove_pieces(skip)
    return board
    
#获取ai模拟移动后产生的所有棋盘
def get_all_moves(path_num,board,color,game):
    boards = []
    valid_moves = board.get_valid_moves(color) #所有棋子可移动位置
    for piece in board.get_all_pieces(color): 
        if piece in valid_moves:
            path_num[0] += 1
            moves = valid_moves[piece]
            show_path(path_num[0],color,piece,board,game,moves)
            for move,skipped in moves.items():
                temp_board = deepcopy(board)#深拷贝，可以对子对象进行复制
                temp_piece = temp_board.pieces[piece.row][piece.col]
                new_board = simulate_move(temp_piece, move,temp_board, skipped)
                boards.append(new_board)
    return boards

#显示搜索路径
def show_path(path_num,color,piece,board,game,valid_moves):
    board.draw(game.win)
    game.draw_turn()
    game.draw_path_num(path_num)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 40, 4)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(500)


