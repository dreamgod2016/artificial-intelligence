#coding: utf-8
import math

first_map = [
'############################################################',  
'#..........................................................#',  
'#.............................#............................#',  
'#.............................#............................#',  
'#.............................#............................#',  
'#.......S.....................#............................#',  
'#.............................#............................#',  
'#.............................#............................#',  
'#.............................#............................#',  
'#.............................#............................#',  
'#.............................#............................#',  
'#.............................#............................#',  
'#.............................#............................#',  
'######..#######################################............#',  
'#....#........#............................................#',  
'#....#........#............................................#',  
'#....###.######............................................#',  
'#....#...#.................................................#',  
'#....#...#.................................................#',  
'#....#####.................................................#',  
'#..........................................................#',  
'#......................................####................#',  
'#...............................########.E####.............#',  
'#...............................#............#.............#',  
'#...............................#............#.............#',  
'#...............................#............#.............#',  
'#...............................#............#.............#',  
'#...............................###########..#.............#',  
'#..........................................................#',  
'#..........................................................#',  
'############################################################']

test_map = []

class Node_Elem:
    """
    
    """
    def __init__(self, parent, x, y, dist):
        self.parent = parent
        self.x = x
        self.y = y
        self.dist = dist

class A_Star:
    """
    docstring for A_Star
    """
    def __init__(self, s_x, s_y, e_x, e_y, width=60, height=30):
        self.s_x = s_x
        self.s_y = s_y
        self.e_x = e_x
        self.e_y = e_y

        self.width = width
        self.height = height

        self.open = []
        self.closed = []
        self.path = []
    
    def find_path(self):
        #查找路径
        p = Node_Elem(None, self.s_x, self.s_y, 0.0)
        while True:
            #A star 算法的特点，所以此处写死循环
            self.extend_round(p)
            #尝试扩展最小的节点
            if not self.open:
                #如果是空的话
                return
            idx, p = self.get_best()
            if self.is_target(p):
                self.make_path(p)
                return
            #把节点压入closed
            self.closed.append(p)
            del self.open[idx]

    def make_path(self, p):
        #从结束点回溯到开始点
        while p:
            self.path.append((p.x, p.y))
            p = p.parent
    def is_target(self, i):
        return i.x == self.e_x and i.y == self.e_y

    def get_best(self):
        better = None
        bv = 100000
        bi = -1
        for idx, i in enumerate(self.open):
            value = self.get_dist(i)
            if value < bv:
                better = i
                bv = value
                bi = idx
        return bi, better

    def get_dist(self, i):
        #核心的计算函数
        # f(x) = g(x) + h(x)
        # g(x)已经固定
        # h(x)估计函数用的是目标位置的距离再×1.5
        return i.dist + math.sqrt((self.e_x-i.x)**2 + (self.e_y-i.y)**2)*1.5

    def extend_round(self, p):
        #各个方向尝试的判断
        #当然 也可以像象棋一样走马啊哈哈哈
        move_xs = (-1,  0,  1, -1, 1, -1, 0, 1)
        move_ys = (-1, -1, -1,  0, 0,  1, 1, 1)

        for x,y in zip(move_xs, move_ys):
            new_x, new_y = x + p.x, y + p.y

            if not self.is_valid_coord(new_x, new_y):
                continue
            #开始尝试新的节点
            node = Node_Elem(p, new_x, new_y, p.dist+self.get_cost(p.x, p.y, new_x, new_y))
            if self.node_in_closed(node):
                continue
            i = self.node_in_open(node)
            if i != -1:
                #如果是-1，就是不在open中
                #如果是其他的数值，就是在open中的某个位置
                if self.open[i].dist > node.dist:
                    self.open[i].parent = p
                    self.open[i].dist = node.dist
                continue
            self.open.append(node)    

    def get_cost(self, x1, y1, x2, y2):
        """
            此处规定计算的代价
        """
        if x1 == x2 or y1 == y2:
            return 1.0
        return 1.5

    def node_in_closed(self, node):
        for n in self.closed:
            if node.x == n.x and node.y == n.y :
                return True
        return False

    def node_in_open(self, node):
        #下面的用法挺有趣的，可以返回索引哈
        for i, n in enumerate(self.open):
            if node.x == n.x and node.y == n.y :
                return i
        return -1

    def is_valid_coord(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return test_map[y][x] != '#'

    def is_valid(self, x, y):
        l = []
        for i in self.open:
            l.append((i.x, i.y))
        for i in self.closed:
            l.append((i.x, i.y))
        return l

    def get_searched(self):
        l = []
        for i in self.open:
            l.append((i.x, i.y))
        for i in self.closed:
            l.append((i.x, i.y))
        return l
    
def print_map():
    """
    打印搜索后的地图
    """    
    for line in test_map:
        print(''.join(line))

def get_start_XY():
    return get_symbol_XY('S')

def get_end_XY():
    return get_symbol_XY('E')

def get_symbol_XY(s):
    for y, line in enumerate(test_map):
        #这里用异常会不会有大的消耗呢
        try:
            x = line.index(s)
        except:
            continue
        else:
            break    
    return x, y

def mark_path(l):
    mark_symbol(l, '*')
      
def mark_searched(l):
    mark_symbol(l, ' ')
      
def mark_symbol(l, s):
    for x, y in l:
        #所以这里的顺序是什么鬼-。-emmm
        test_map[y][x] = s  
      
def mark_start_end(s_x, s_y, e_x, e_y):  
    test_map[s_y][s_x] = 'S'  
    test_map[e_y][e_x] = 'E'  
      
def tm_to_test_map():  
    for line in first_map:
        test_map.append(list(line))  

def find_path():  
    s_x, s_y = get_start_XY()  
    e_x, e_y = get_end_XY()  
    a_star = A_Star(s_x, s_y, e_x, e_y)  
    a_star.find_path()  
    searched = a_star.get_searched()  
    path = a_star.path  
    #标记已搜索区域  
    mark_searched(searched)  
    #标记路径  
    mark_path(path)  
    print("path length is %d"%(len(path)))
    print("searched squares count is %d"%(len(searched)))
    #标记开始、结束点  
    mark_start_end(s_x, s_y, e_x, e_y)  
      
if __name__ == "__main__":  
    #把字符串转成列表  
    tm_to_test_map()  
    find_path()  
    print_map()