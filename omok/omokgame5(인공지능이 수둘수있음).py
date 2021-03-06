import pygame, sys
from pygame.locals import *
from tensorflow.keras.models import load_model
import numpy as np
from time import sleep

pygame.init()
### 인공지능턴에 다음 수 예측할때 사용할 모델###
model = load_model('C:/data/omok/modelcheckpoint/0216_mymodel.h5')

# h=15
# w=15
# input = np.zeros((15,15),dtype=np.int)
# input[13][5] = 1
# input[13][4] = 2
# input[14][8] = 1
# input[14][7] = 2
# input[12][6] = 1

# print(input)
# input[(input != 1) & (input != 0)] = -1
# input[(input == 1) & (input != 0)] = 1
# input = np.expand_dims(input, axis=(0, -1)).astype(np.float32)

# output = model.predict(input).squeeze()
# output = output.reshape((h, w))
# output_y, output_x = np.unravel_index(np.argmax(output), output.shape)
# print(output_y, output_x)


omokpan = pygame.image.load('C:/data/omok/image/board.png')
white_stone = pygame.image.load('C:/data/omok/image/white.png')
black_stone = pygame.image.load('C:/data/omok/image/black.png')

omokpan_size = omokpan.get_rect().size # 사이즈 가져오기
omokpan_w = omokpan_size[0] # 가로 크기
omokpan_h = omokpan_size[1] # 세로 크기

window_w = 501
window_h = 501

print(omokpan_w,omokpan_h) #501,501
omokpan_x_position = (window_w / 2) - (omokpan_w / 2) 
omokpan_y_position = (window_h / 2) - (omokpan_h / 2)   

fps = 60 # frames per second setting
fps_clock = pygame.time.Clock()

dis_surf = pygame.display.set_mode((501, 501))
pygame.display.set_caption('오목')
font = pygame.font.SysFont("consolas",20)

##########색 정의
board_color1 = (153, 102, 000)
board_color2 = (153, 102, 51)
board_color3 = (204, 153, 000)
board_color4 = (204, 153, 51)
bg_color = (128, 128, 128)  #gray color
black = (0, 0, 0)
blue = (0, 50, 255)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)

#########사이즈 정의
window_w = 501
window_h = 501
board_size = 15
grid_size = 30
black = 1
white = 2


class Board(object):
    def __init__(self):
        self.x = window_w
        self.y = window_h
        self.board_image = omokpan
        self.pixel_coords  = []
        self.white_image = pygame.transform.scale(white_stone, (grid_size, grid_size))
        self.black_image = pygame.transform.scale(black_stone, (grid_size, grid_size))
        
        self.board_ary = [[0 for i in range(board_size)] for j in range(board_size)]

    def init_board(self):
        for y in range(board_size):
            for x in range(board_size):
                self.board_ary[y][x] = 0   ##보드를 0으로 초기화

    def draw_board(self):
        dis_surf.blit(self.board_image,(0,0))

    def draw_w_stone(self, x_stone_position,y_stone_position):
        player = 2
        x = x_stone_position * grid_size + 25
        y = y_stone_position * grid_size + 25 
        
        self.w_stone_image = white_stone
        img = self.white_image
        dis_surf.blit(img,(x,y))
        

    def draw_b_stone(self,x_stone_position,y_stone_position):
        player = 1
        x = x_stone_position * grid_size + 25
        y = y_stone_position * grid_size + 25
        
        self.b_stone_image = black_stone
        img = self.black_image
        dis_surf.blit(img,(x,y))
        
        

    ###픽셀 좌표 구하는 함수##
    #x,y좌표에다가 격자크기만큼 곱해주면 됨.
    def set_coords(self):
        for y in range(board_size):
            for x in range(board_size):
                self.pixel_coords.append((x * grid_size + 25, y * grid_size + 25))
    
    
#마우스 포인트 좌표를 넘겨받아 픽셀 좌표들과 비교하여 마우스 포인트 좌표가 위치한 곳을 찾는 함수 
#찾이 못하면 none 리턴
    def get_coord(self, pos):
        for coord in self.pixel_coords:
            x, y = coord
            rect = pygame.Rect(x, y, grid_size, grid_size)
            if rect.collidepoint(pos):
                return coord
        return None

    def get_point(self, coord):
        x, y = coord
        x = (x - 25) // grid_size
        y = (y - 25) // grid_size
        return x, y

class Game_Rule(object):
    #차례 바꿔주는 함수
    def turn(self,player):
        self.player = player
        if self.player == 1:
            player = 2
            return player
        elif self.player == 2:
            player = 1
            return player
 
        


def main():
    board = Board()
    game_rule = Game_Rule()
    #stone_list = []    # 빈 리스트 생성

    # for i in range(15):
    #     line = []              # 안쪽 리스트로 사용할 빈 리스트 생성
    #     for j in range(15):
    #         line.append(0)     # 안쪽 리스트에 0 추가
    #     stone_list.append(line)         # 전체 리스트에 안쪽 리스트를 추가

    # print(stone_list)

    #coord = board.get_coord()
    #x, y = board.get_point(coord)
    player = 1 #1이 white 2가 black
    button = None
    stone_list = np.zeros((15,15),dtype=np.int)
    stone_ary = np.zeros((15,15),dtype=np.int)

    # x_stone_position = window_w/2
    # y_stone_position = window_h/2
    while True:
        fps_clock.tick(fps)
        #event = pygame.event.poll() #이벤트 처리
        board.draw_board()
        board.init_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                player=1
                x_stone_position = event.pos[0] // grid_size - 1
                y_stone_position = event.pos[1] // grid_size - 1
                print("내가 놓은 위치는:",x_stone_position, y_stone_position)  #왼쪽 가장 위가 1,1
                sleep(0.1)
                #game_rule.turn(player_num)
                stone_list[y_stone_position][x_stone_position] = player
                stone_ary[y_stone_position][x_stone_position] = player  #수를 둔 좌표에 15x15배열상태에 플레이어별로 저장
                print(stone_ary)

                player = -1  #player update
                stone_ary2 = np.expand_dims(stone_ary, axis=(0, -1)).astype(np.float32)
                pred = model.predict(stone_ary2).squeeze()
                pred = pred.reshape((15, 15))
                pred_y, pred_x = np.unravel_index(np.argmax(pred), pred.shape)
                print("인공지능이 예측한 다음수는 ",pred_x, pred_y,"입니다")

                stone_list[pred_y][pred_x] = player
                stone_ary[pred_y][pred_x] = player

                print("======oneclick end=======")

            for y_stone_position in range(board_size):
                for x_stone_position in range(board_size):
                    player_num = stone_list[y_stone_position][x_stone_position]
                    if player_num ==1 : 
                        board.draw_b_stone(x_stone_position,y_stone_position)
                    
            for pred_y in range(board_size):
                for pred_x in range(board_size):
                    player_num = stone_list[pred_y][pred_x]
                    if player_num == -1:
                        board.draw_w_stone(pred_x,pred_y)

            # for y_stone_position in range(board_size):
            #     for x_stone_position in range(board_size):
            #         player_num = stone_list[x_stone_position][y_stone_position]
                    
            #         if player_num == 1:
            #             board.draw_b_stone(x_stone_position,y_stone_position)
            #             sleep(0.1)
            #             player=2
            #             #game_rule.turn(player_num)
                        
            #         elif player_num == 2:
            #             board.draw_w_stone(x_stone_position,y_stone_position)
            #             sleep(0.1)
            #             player = 1
            #             #game_rule.turn(player_num)
                        

            pygame.display.update()
            fps_clock.tick(fps)

if __name__ == "__main__":
    main()

#0,0 -> 7,7
#14,14 -> 2,1
#14,0 ->5,7   14->0 8,7 이나와야함
#0,14 ->7,8