#coding : utf-8
# n皇后问题的退火算法
import random
import math

def get_cost(board):
    #f()判断当前cost
    cost = 0
    for i in range(len(board)):
        for j in range(i + 1,len(board)):
            #开始判断是否有碰撞
            if board[i] == board[j]:
                cost += 1
            #判断对角线上是否有碰撞
            offset = j - i
            if board[i] == board[j] + offset or board[i] == board[j] - offset:
                cost += 1
    return cost

def make_annealing_move(board, cost_to_beat, temp):
    board_copy = list(board)
    found_move = False
    while not found_move:
        #这里写的可能是死循环，但是总会走一步的吧
        board_copy = list(board)
        #如果尝试失败，可以回溯到上一个状态
        new_row = random.randint(0, len(board)-1)
        new_col = random.randint(0, len(board)-1)
        board_copy[new_col] = new_row
        new_cost = get_cost(board_copy)
        if new_cost < cost_to_beat:
            found_move = True
        else:
            #接下来是概率采用
            delta_e = cost_to_beat - new_cost
            #
            accpet_probability = min(1, math.exp(delta_e/temp))
            found_move = random.random() <= accpet_probability
    return board_copy

def print_board(soln , nr):
    for i in range(nr):
        row = ['~']*nr
        for col in range(nr):
            if soln[col] == nr-i-1:
                row[col] = 'Q'
        print(' '.join(row))

def annealing(board):
    temp = len(board)**2
    #和board成平方的关系
    anneal_rate = 0.95
    new_cost = get_cost(board)
    steps = 0
    while new_cost > 0:
        #cost一直没有到零，到零就是结束了.
        board = make_annealing_move(board, new_cost, temp)
        new_cost = get_cost(board)
        #temp也可以变变？
        temp = max(temp * anneal_rate, 0.01)
        steps += 1
        if steps >= 50000:
            #倒霉到50000次都没算出来结果
            break
    print_board(board, len(board))
def annealingAlgo(num):
    board = [random.randint(0,num-1) for i in range(num)]
    annealing(board)

if __name__ == '__main__':
    annealingAlgo(80)