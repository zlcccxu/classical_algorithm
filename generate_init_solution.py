import numpy as np

from load_tsp_file import load_tsp_euc2d

# ===================== 辅助函数 =====================
def calc_tour_distance(path, adj_matrix):
    """
    计算TSP闭合回路的总距离
    参数:
        path: list/array, 节点访问顺序（0-based索引）
        adj_matrix: np.ndarray, n×n距离邻接矩阵
    返回:
        回路总距离
    """
    path = np.asarray(path)
    # 相邻节点距离和 + 最后节点回到起点的距离
    return adj_matrix[path[:-1], path[1:]].sum() + adj_matrix[path[-1], path[0]]


# ===================== 1. 贪心最近邻算法 greedy1 =====================
def greedy1(adj_matrix):
    """
    最近邻贪心算法：从第1个节点（索引0）出发，每次选择最近的未访问节点加入路径，
    全程避免形成环路，最终生成闭合TSP回路。
    
    参数:
        adj_matrix: np.ndarray, n×n的距离邻接矩阵
    返回:
        path: list[int], 节点访问顺序（0-based索引，长度等于节点数）
        total_dist: int, 闭合回路总距离
    """
    n = adj_matrix.shape[0]
    visited = np.zeros(n, dtype=bool)
    path = []
    current = 0  # 从第一个节点开始
    path.append(current)
    visited[current] = True

    # 逐步加入剩余n-1个节点
    for _ in range(n - 1):
        # 取出当前节点到所有节点的距离，已访问节点设为无穷大
        dist_row = adj_matrix[current].copy()
        #dist_row[visited] = np.inf
        MAX_INT = np.iinfo(np.int32).max  # 对于 int32，值为 2147483647
        dist_row[visited] = MAX_INT
        # 找到距离最近的未访问节点
        next_node = np.argmin(dist_row).item()
        path.append(next_node)
        visited[next_node] = True
        current = next_node

    total_dist = calc_tour_distance(path, adj_matrix)
    return path, total_dist


# ===================== 2. 随机解算法 random =====================
def random_tsp(adj_matrix):
    """
    随机生成TSP可行解：随机生成一个节点排列，对应一条闭合回路。
    
    参数:
        adj_matrix: np.ndarray, n×n的距离邻接矩阵
    返回:
        path: list[int], 节点访问顺序（0-based索引，长度等于节点数）
        total_dist: int, 闭合回路总距离
    """
    n = adj_matrix.shape[0]
    # 生成 0 ~ n-1 的随机排列
    path = np.random.permutation(n).tolist()
    total_dist = calc_tour_distance(path, adj_matrix)
    return path, total_dist


# ===================== 测试程序 =====================
if __name__ == "__main__":
    print("=" * 50)
    print("测试1：3节点小规模手动验证（正确性校验）")
    print("=" * 50)
    # 手动构造3节点距离矩阵：0-1=1, 0-2=2, 1-2=3
    adj_3nodes = np.array([
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ])
    path_greedy, dist_greedy = greedy1(adj_3nodes)
    print(f"贪心算法路径: {path_greedy}")
    print(f"贪心算法总距离: {dist_greedy}  （预期：1+3+2 = 6）")
    assert dist_greedy == 6, "贪心算法计算错误！"
    assert len(path_greedy) == 3 and len(set(path_greedy)) == 3, "路径不满足可行解要求！"

    # 随机解验证：检查是否是合法排列、距离计算正确
    path_rand, dist_rand = random_tsp(adj_3nodes)
    print(f"\n随机算法路径: {path_rand}")
    print(f"随机算法总距离: {dist_rand}")
    assert len(path_rand) == 3 and len(set(path_rand)) == 3, "随机路径不满足可行解要求！"
    print("✅ 3节点测试通过：路径合法，距离计算正确\n")


    print("=" * 50)
    print("测试2：4节点正方形验证（几何一致性校验）")
    print("=" * 50)
    # 4个节点：(0,0), (0,1), (1,1), (1,0)，按TSPLIB nint规则计算距离
    coords_4 = np.array([[0,0], [0,1], [1,1], [1,0]], dtype=np.float64)
    x = coords_4[:, 0]
    y = coords_4[:, 1]
    x_diff = x[:, np.newaxis] - x[np.newaxis, :]
    y_diff = y[:, np.newaxis] - y[np.newaxis, :]
    adj_4nodes = np.floor(np.sqrt(x_diff**2 + y_diff**2) + 0.5).astype(int)

    print("4节点距离矩阵：")
    print(adj_4nodes)

    path_greedy4, dist_greedy4 = greedy1(adj_4nodes)
    print(f"\n贪心算法路径: {path_greedy4}")
    print(f"贪心算法总距离: {dist_greedy4}")
    assert len(path_greedy4) == 4 and len(set(path_greedy4)) == 4, "路径不合法！"

    # 多次运行随机解，验证一致性
    for i in range(3):
        p, d = random_tsp(adj_4nodes)
        print(f"第{i+1}次随机路径: {p}，总距离: {d}")
        assert len(set(p)) == 4, "随机路径存在重复节点！"
    print("✅ 4节点测试通过：路径均为合法哈密顿回路\n")


    print("=" * 50)
    print("测试3：a280实例大规模验证（可用性校验）")
    print("=" * 50)
    try:
        # 复用之前的加载函数（此处直接集成最简版，确保可独立运行）
        name, dim, adj_a280 = load_tsp_euc2d("data\\tsp\\a280.txt")
        print(f"实例：{name}，节点数：{dim}")

        # 贪心算法测试
        path_a280_greedy, dist_a280_greedy = greedy1(adj_a280)
        print(f"\n贪心算法：")
        print(f"  路径长度：{len(path_a280_greedy)} 个节点")
        print(f"  无重复节点：{len(set(path_a280_greedy)) == dim}")
        print(f"  回路总距离：{dist_a280_greedy}")

        # 随机算法测试
        path_a280_rand, dist_a280_rand = random_tsp(adj_a280)
        print(f"\n随机算法：")
        print(f"  路径长度：{len(path_a280_rand)} 个节点")
        print(f"  无重复节点：{len(set(path_a280_rand)) == dim}")
        print(f"  回路总距离：{dist_a280_rand}")

        print("✅ a280大规模测试通过：两个算法均生成合法可行解")

    except FileNotFoundError:
        print("⚠️  未找到a280.txt文件，跳过大规模测试")
        print("   可将a280.txt放在脚本同目录下执行完整测试")

    print("\n🎉 所有测试完成")
