import numpy as np

def load_tsp_euc2d(file_path):
    """
    读取EUC_2D类型的TSPLIB坐标文件，返回实例信息与NumPy格式的距离邻接矩阵

    参数:
        file_path: str，TSP实例文件的路径
    返回:
        name: str，实例名称（如a280）
        dimension: int，节点总数
        adj_matrix: np.ndarray，dimension×dimension的二维整数数组
                    adj_matrix[i][j] 表示第 i+1 号节点与第 j+1 号节点的距离
                    距离公式: dij = nint( sqrt( (xi-xj)² + (yi-yj)² ) )
    """
    name = None
    dimension = None
    coordinates = []
    in_coord_section = False

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # 解析实例名称
            if line.upper().startswith('NAME'):
                name = line.split(':', 1)[1].strip()

            # 解析节点维度
            elif line.upper().startswith('DIMENSION'):
                dimension = int(line.split(':', 1)[1].strip())

            # 进入坐标数据段
            elif line.upper() == 'NODE_COORD_SECTION':
                in_coord_section = True
                continue

            # 文件结束标记
            elif line.upper() == 'EOF':
                break

            # 逐行解析节点坐标
            elif in_coord_section:
                parts = line.split()
                x = float(parts[1])
                y = float(parts[2])
                coordinates.append((x, y))

    # 校验坐标数量与维度一致
    if len(coordinates) != dimension:
        raise ValueError(
            f"坐标数量({len(coordinates)})与声明维度({dimension})不匹配"
        )

    # 转换为NumPy数组，向量化计算距离矩阵
    coords = np.array(coordinates, dtype=np.float64)
    x = coords[:, 0]
    y = coords[:, 1]

    # 广播机制：一次性计算所有点对的横纵坐标差，生成 dimension×dimension 矩阵
    x_diff = x[:, np.newaxis] - x[np.newaxis, :]
    y_diff = y[:, np.newaxis] - y[np.newaxis, :]

    # 计算欧氏距离并执行 TSPLIB 标准 nint 取整（0.5向上取整，规避银行家舍入）
    dist_matrix = np.sqrt(x_diff ** 2 + y_diff ** 2)
    adj_matrix = np.floor(dist_matrix + 0.5).astype(np.int32)

    return name, dimension, adj_matrix


# ========== 测试程序 ==========
if __name__ == "__main__":
    try:
        name, dim, adj = load_tsp_euc2d("data\\tsp\\a280.txt")
        print("===== 函数测试结果 =====")
        print(f"实例名称(Name): {name}")
        print(f"节点数量(Dimension): {dim}")
        print(f"邻接矩阵类型: {type(adj)}")
        print(f"邻接矩阵维度: {adj.shape}")
        print(f"邻接矩阵数据类型: {adj.dtype}")
        print("-" * 40)

        # 验证1：对角线（节点到自身）距离全为0
        diag_all_zero = np.all(np.diag(adj) == 0)
        print(f"1. 节点自环距离全为0：{diag_all_zero}  （预期：True）")

        # 验证2：距离矩阵对称性
        is_symmetric = np.array_equal(adj, adj.T)
        print(f"2. 距离矩阵对称：{is_symmetric}  （预期：True）")

        # 验证3：手动抽样校验距离值（与纯Python版本完全一致）
        print("3. 手动抽样距离校验：")
        # 节点1 (288,149) ↔ 节点2 (288,129) → 垂直距离20
        print(f"   节点1 ↔ 节点2: {adj[0, 1]}  （预期：20）")

        # 节点1 (288,149) ↔ 节点3 (270,133) → sqrt(18²+16²)=√580≈24.08 → 24
        print(f"   节点1 ↔ 节点3: {adj[0, 2]}  （预期：24）")

        # 节点76 (16,57) ↔ 节点77 (8,49) → sqrt(8²+8²)=√128≈11.31 → 11
        print(f"   节点76 ↔ 节点77: {adj[75, 76]}  （预期：11）")

        print("\n测试完成！NumPy向量化版本运行正常。")

    except FileNotFoundError:
        print("错误：未找到 data\\tsp\\a280.txt 文件，请将文件放在脚本同目录下。")
    except Exception as e:
        print(f"运行出错: {e}")
