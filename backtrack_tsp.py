import numpy as np

from generate_init_solution import greedy1
from load_tsp_file import load_tsp_euc2d

def calc_tour_distance(path, adj_matrix):
    path = np.asarray(path)
    return adj_matrix[path[:-1], path[1:]].sum() + adj_matrix[path[-1], path[0]]


def get_two_smallest(row):
    """取一行中最小的两个非零距离，用于LB2界函数"""
    arr = row[row>0]
    a = np.partition(arr,1)[:2]
    return a[0], a[1]


def bound_lb2(cur, visited, adj):
    """
    界函数LB2：最小两条边之和的一半，完整回路下界
    返回：整个完整回路代价的下界
    """
    n = adj.shape[0]
    s = 0.0
    for u in range(n):
        d1,d2 = get_two_smallest(adj[u,:])
        s += d1 + d2
    return s / 2.0


# 回溯主函数，封装，避免全局变量
def tsp_backtrack_with_bound(adj):
    n = adj.shape[0]
    # 使用贪心得到初始上界，极大加速剪枝
    greedy_path, greedy_dist = greedy1(adj)
    best_cost = greedy_dist
    best_path = greedy_path.copy()

    visited = np.zeros(n, dtype=bool)
    path = [0]
    visited[0] = True

    def backtrack(path_, visited_, curr_cost):
        nonlocal best_cost, best_path
        cur = path_[-1]
        if len(path_) == n:
            total = curr_cost + adj[cur, 0]
            if total < best_cost:
                best_cost = total
                best_path = path_.copy()
            return

        lb = bound_lb2(cur, visited_, adj)
        if curr_cost >= lb and curr_cost >= best_cost:
            return

        for v in range(n):
            if not visited_[v]:
                visited_[v] = True
                path_.append(v)
                backtrack(path_, visited_, curr_cost + adj[cur, v])
                path_.pop()
                visited_[v] = False

    backtrack(path, visited, 0)
    return best_path, best_cost



if __name__ == "__main__":
    # 小规模测试：4节点
    adj_4 = np.array([
        [0,1,2,3],
        [1,0,4,5],
        [2,4,0,6],
        [3,5,6,0]
    ])
    name, dim, adj = load_tsp_euc2d("data\\tsp\\a280.txt")#节点太多，回溯法会非常慢，建议使用小规模实例进行测试
    best_p, best_d = tsp_backtrack_with_bound(adj_4)
    print(f"回溯带界最优路径:{best_p},最优距离:{best_d}")
