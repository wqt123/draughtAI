import pygame
from config import ROWS,COLS,SIZE,BLACK,WHITE,WIDTH,HEIGHT,BLUE,GREEN,GREY1,GREY2,WHITE_CROWN,BLACK_CROWN

#棋子类
class Piece:
    PADDING = 10 #棋子与棋格轮廓的距离
    def __init__(self,row,col,color):
        self.row = row #棋子所在行
        self.col = col #棋子所在列
        self.color = color #棋子颜色
        self.is_king = False#棋子是否成“王”，成王棋子可以向后移动
        self.x = SIZE*self.col + SIZE // 2     #棋子x轴坐标
        self.y = SIZE*self.row + SIZE // 2     #棋子y轴坐标

    #绘制棋子
    def draw_piece(self,win):
        pygame.draw.circle(win,GREY2,(self.x,self.y),SIZE//2 -self.PADDING + 2)
        pygame.draw.circle(win,self.color,(self.x,self.y),SIZE//2 -self.PADDING)
        if self.is_king:
            #绘制王冠
            if self.color == WHITE: 
                win.blit(WHITE_CROWN, (self.x - WHITE_CROWN.get_width()//2, self.y - WHITE_CROWN.get_height()//2 - 3))
            else:
                win.blit(BLACK_CROWN, (self.x - BLACK_CROWN.get_width()//2, self.y - BLACK_CROWN.get_height()//2 - 3))
    
    #移动棋子
    def _move(self,row,col):
        self.row = row
        self.col = col
        self.x = SIZE*self.col + SIZE // 2     
        self.y = SIZE*self.row + SIZE // 2     


dir_move = [[-1,-1],[-1,1],[1,-1],[1,1]]
dir_jump = [[-2,-2],[-2,2],[2,-2],[2,2]]
#棋盘类
class Board:
    def __init__(self):
        self.pieces = [] #存储棋盘中所有棋子
        self.white_kings = self.black_kings = 0 #双方变成“王”的棋子数
        self.white_left  = self.black_left = 12#双方剩余棋子数
        self.init_pieces()
        self.is_jump = False #棋盘中是否有棋子可以吃子
        self.longest_num = 0 #当前棋盘中棋子能吃的最多棋子数
    
    #初始化棋子
    def init_pieces(self): 
        for row in range(ROWS):
            self.pieces.append([])
            for col in range(COLS):
                if (row + 1) % 2 == col % 2: #棋子间隔摆放
                    if row < 3:
                        self.pieces[row].append(Piece(row,col,BLACK))
                    elif row < 5:
                        self.pieces[row].append(0)
                    else:
                        self.pieces[row].append(Piece(row,col,WHITE))
                else:
                    self.pieces[row].append(0)
    
    #绘制棋盘           
    def draw(self,win):
        win.fill(GREY1)
         #交替绘制两种颜色棋格
        for row in range(ROWS):
            for col in range((row +1) % 2,ROWS,2): 
                pygame.draw.rect(win,GREEN,(row*SIZE,col*SIZE,SIZE,SIZE))

        for i in range(len(self.pieces)):
            for j in range(len(self.pieces[i])):
                if self.pieces[i][j]:
                    self.pieces[i][j].draw_piece(win)
   
    #加冕到达边线的棋子
    def make_king(self,row,piece):
        if row == ROWS - 1 or row == 0:
            piece.is_king =  True
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1 
    
    #移动棋子
    def move_piece(self,piece,row,col):
        '''
        将选择的棋子移动至相应位置，并检查棋子是否能够加冕
        '''
        self.pieces[piece.row][piece.col], self.pieces[row][col] = self.pieces[row][col], self.pieces[piece.row][piece.col]
        piece._move(row, col)
        self.make_king(row, piece)
    #删除棋子
    def remove_pieces(self,skipped):
        '''
        当发生吃子时，将被吃棋子删除
        '''
        for p in skipped:
            self.pieces[p.row][p.col] = 0
            if p.color == WHITE:
                self.white_left -= 1
            if p.color == BLACK:
                self.black_left -= 1
    
    #判断是否在棋盘中
    def is_in_board(self,row,col):
        if row < 0 or row >= ROWS or col < 0 or col >= COLS:
            return False
        return True
    
    #获取吃子后位置
    def try_to_jump(self,row,col,is_king,color,step_num,skipped = []):
        global dir_jump
        moves = {}
        piece = self.pieces[row][col]
        #根据棋子属性决定可移动位置
        if is_king:
            start = 0
            stop = 4
        elif color == WHITE:
            start = 0
            stop = 2
        else:
            start = 2
            stop = 4

        for i in range(start,stop):
            new_row = row + dir_jump[i][0]
            new_col = col + dir_jump[i][1]
            mid_row = (row + new_row) //2
            mid_col = (col + new_col) //2
            if self.is_in_board(new_row,new_col):
                new_piece = self.pieces[new_row][new_col]
            else:
                continue
            #如果满足吃子条件
            if new_piece == 0 and self.pieces[mid_row][mid_col] and self.pieces[mid_row][mid_col].color != color:        
                #一个棋子只能被跳跃一次，当棋子已经被跳过时，跳过本次循环
                if self.pieces[mid_row][mid_col] in skipped: 
                   continue
                self.is_jump = True
                #更新最长路径
                if step_num > self.longest_num:
                    self.longest_num = step_num
                last = skipped.copy()
                last += [self.pieces[mid_row][mid_col]]
                #在吃子后的位置继续搜索
                moves.update(self.try_to_jump(new_row, new_col,is_king,color,step_num + 1,last))
        if skipped:
            moves[(row,col)] = skipped

            
        return moves
    
    #获取可移动位置
    def try_to_move(self,row,col):
        global dir_move
        moves = {}
        piece = self.pieces[row][col]
        #根据棋子属性决定可移动位置
        if piece.is_king:
            start = 0
            stop = 4
        elif piece.color == WHITE:
            start = 0
            stop = 2
        else:
            start = 2
            stop = 4
        for i in range(start ,stop):
            new_row = row + dir_move[i][0]
            new_col = col + dir_move[i][1]
            if self.is_in_board(new_row,new_col):
                new_piece = self.pieces[new_row][new_col]
            else:
                continue
            if new_piece == 0:
                moves[(new_row,new_col)] = []

        return moves
    
        #判断是否有人赢得对局
    
    #返回胜者
    def winner(self):
        if self.white_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return WHITE
        else:
            return None
    
    #获取当前回合走棋方的所有棋子
    def get_all_pieces(self,color):
        pieces = []
        for row in self.pieces:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    #获取棋子当前可移动的所有位置
    def get_valid_moves(self,color):
        valid_moves = {} #字典记录所有棋子可移动的路径
        self.is_jump = False
        #先搜索是否可以吃子
        for piece in self.get_all_pieces(color):
            moves = {}
            moves.update(self.try_to_jump(piece.row,piece.col,piece.is_king,piece.color,1))
            if moves:
                valid_moves[piece] = moves
        #如不能吃子，获取棋子可移动位置
        if not self.is_jump: 
            for piece in self.get_all_pieces(color):
                moves = {}
                moves.update(self.try_to_move(piece.row,piece.col))
                if moves:
                    valid_moves[piece] = moves
            
        valid_moves_ = {} #记录所有的最长路径
        if self.is_jump:
            for piece,moves in valid_moves.items():
                _moves_ = {}
                for move,skipped in moves.items():
                    moves_ = {}
                    if skipped:
                        #在所有路径中选择最长的
                        if len(skipped) == self.longest_num:
                            moves_[move] = skipped  
                            _moves_.update(moves_) 
                            valid_moves_[piece] = _moves_
        else:
            valid_moves_ = valid_moves
        return valid_moves_

    #评估函数
    def evaluate(self,color):
        score = self.white_left - self.black_left + (self.white_kings * 0.5 - self.black_kings * 0.5)
        if color == WHITE:
            return -score
        else:
            return score
    

class Game:
    def __init__(self,win,my_turn):
        self.init(win,my_turn)

    #初始化Game类参数
    def init(self,win,my_turn):
        self.selected_piece = None #被选中的棋子
        self.turn = WHITE #当前要移动的棋子颜色，白子先行
        self.valid_moves_ = {} #走棋方所有棋子可移动的位置
        self.valid_moves = {} #当前选中棋子可移至的位置
        self.board = Board()  #棋盘
        self.win = win        #游戏窗口
        self.my_turn = my_turn #玩家棋子的颜色
    
    #返回胜者
    def winner(self):
        return self.board.winner()
    #更新游戏画面
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        self.draw_turn()
        self.draw_path_num()
        pygame.display.update()

    #绘制棋子可以移至的位置
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SIZE + SIZE//2, row * SIZE + SIZE//2), 15)
    
    #显示当前走棋方
    def draw_turn(self):
        if self.turn == WHITE:
            turn_text = 'Turn：WHITE'
        else:
            turn_text = 'Turn：BLACK'
        font = pygame.font.SysFont('simhei', 30)
        turn = font.render(turn_text, True, (0,0,0))
        self.win.blit(turn, (30, HEIGHT - 35))
    
    #显示对抗搜索算法已经搜索过的节点数
    def draw_path_num(self,num = 0):
        if self.turn == self.my_turn:
            text = 'Path Num：-'
        else:
            text = 'Path Num：' + str(num)
        font = pygame.font.SysFont('simhei', 30)
        text_num = font.render(text, True, (0,0,0))
        self.win.blit(text_num, (WIDTH/2 + 30, HEIGHT - 35))
    
    #显示胜负
    def draw_winner(self):
        if self.board.winner() == None:
            return
        if  self.board.winner() == WHITE:
            text = '白方获胜，游戏结束！'
        else:
            text = '黑方获胜，游戏结束！'
        font = pygame.font.SysFont('simhei', 32)
        gameover_text = font.render(text, True, (255,0,0))
        self.win.blit(gameover_text, (WIDTH / 4,HEIGHT / 2 - 20))
        pygame.display.update()
        pygame.time.delay(3000)
        
    
    #点击后选中棋子或移动
    def after_click(self,row,col): 
        '''
         如果棋盘已有棋子被选中，则移动该棋子；反之，选中该棋子
         当移动失败时(选中的移动位置不符合游戏规则)：
         重新选中棋子
        ''' 
        if self.selected_piece:
            if not self.move(row,col):
                self.selected_piece = None
                self.after_click(row, col)
        else:                   
            piece = self.board.pieces[row][col]
            if piece != 0 and (piece.color == self.turn):
                self.selected_piece = piece
                if piece in self.valid_moves_:
                    self.valid_moves = self.valid_moves_[piece]
                else:
                    self.valid_moves = {}

    def get_moves(self):
        self.valid_moves_ = self.board.get_valid_moves(self.turn)


    #棋子移动逻辑
    def move(self,row,col):
        '''
         如果棋子不可移动到选中位置，移动失败，返回False
         反之移动棋子至选中位置，并检查是否进行了吃子，将被吃的棋子删除，移动成功，返回True
        '''
        piece = self.board.pieces[row][col]
        if self.selected_piece and piece == 0 and self.valid_moves and (row,col) in self.valid_moves:
            self.board.move_piece(self.selected_piece, row, col)
            if self.board.is_jump:
                skipped = self.valid_moves[(row,col)]
                self.board.remove_pieces(skipped)
            self.change_turn()
            return True
        return False
    
    #改变走棋方
    def change_turn(self):
        self.board.longest_num = 0
        self.valid_moves = {}
        self.valid_moves_ = {}
        self.selected_piece = None
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
    
    #ai进行走棋
    def ai_move(self,board):
        self.board = board
        self.change_turn()    