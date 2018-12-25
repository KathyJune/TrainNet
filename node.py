# -*- encoding: utf-8 -*-
class Path:
    def __init__(self):
        self.nodes = []
        self.dis = 0


class PathSolve:
    def __init__(self):
        self.path = Path()
        self.paths = []
        self.nodes = {}

    def is_node_in_path(self, input_node):
        for node in self.path.nodes:
            if node == input_node:
                return True
        return False

    def save_path(self):
        path_temp = []
        for node in self.path.nodes:
            path_temp.append(node)
        self.paths.append([path_temp, self.path.dis])

    # find all possible paths
    # cnode: currentNode
    # pnode: previousNode of the currentNode
    # snode: startNode
    # enode: endNode
    def solve(self, cnode, pnode, snode, enode):
        # if the condiiton is matched, a loop is generated, then return false
        if (cnode is not None) and (pnode is not None) and (cnode == pnode):
            return False
        if cnode is not None:
            i = 0
            # get startnode in path
            self.path.nodes.append(cnode)
            if pnode is not None:
                self.path.dis += self.nodes[pnode][cnode]
            # if the current node is the end node, save the path
            if cnode == enode:
                self.save_path()
                return True
            else:
                keys1 = list(self.nodes[cnode].keys())
                nnode = keys1[i]
                while nnode is not None:
                    # 如果nNode是最初的起始节点或者nNode就是cNode的上一节点或者nNode已经在栈中 ，
                    # 说明产生环路 ，应重新在与当前起始节点有连接关系的节点集中寻找nNode
                    if (pnode is not None) and (nnode == snode or nnode == pnode or self.is_node_in_path(nnode)):
                        i += 1
                        keys2 = list(self.nodes[cnode].keys())
                        if i > (len(keys2) - 1):
                            nnode = None
                        else:
                            keys3 = list(self.nodes[cnode].keys())
                            nnode = keys3[i]
                        continue
                    if self.solve(nnode, cnode, snode, enode):  # 递归调用
                        # 如果找到一条路径，则弹出栈顶节点
                        self.path.nodes.pop(len(self.path.nodes) - 1)
                        self.path.dis -= self.nodes[cnode][nnode]
                    # 继续在与cNode有连接关系的节点集中测试nNode
                    i += 1
                    keys4 = list(self.nodes[cnode].keys())
                    if i > (len(keys4) - 1):
                        nnode = None
                    else:
                        nnode = keys4[i]
                n = len(self.path.nodes)
                if n > 1:
                    self.path.dis -= self.nodes[self.path.nodes[n - 1]
                                                ][self.path.nodes[n - 2]]
                self.path.nodes.pop(len(self.path.nodes) - 1)
                return False
        else:
            return False

# for test
# if __name__ == '__main__':
#     nodes = {'0': {'1': 1}, '1': {'0': 1, '5': 5, '2': 2, '3': 3}, '2': {'1': 2, '4': 4}, '3': {'1': 3, '4': 4},\
#              '4': {'2': 4, '3': 4, '5': 5}, '5': {'1': 5, '4': 5}}
#     solve = PathSolve(nodes)
#     code1 = '0'
#     scode = '0'
#     ecode = '4'
#     solve.solve(code1, None, scode, ecode)
#     a = 1
