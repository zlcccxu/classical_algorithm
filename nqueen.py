def solve_n_queens(n):
    """
    N皇后回溯，行、列下标从1开始
    空间换时间：col_used, diag1, diag2 实现 O(1) 冲突检查
    :param n: n×n棋盘
    :return: 所有解，每个解queen[1..n]，queen[i] = 第i行皇后的列号
    """
    result = []
    # queen[0]闲置不用，queen[1]~queen[n]有效
    queen = [0] * (n + 1)

    # 标记占用：列、主对角线、副对角线
    col_used = [False] * (n + 1)
    diag1 = [False] * (2 * n)   # diag1 = row - col + n ∈ [1, 2n-1]
    diag2 = [False] * (2 * n + 2) # diag2 = row + col ∈ [2, 2n]

    def backtrack(row):
        # row：当前放置第 row 个皇后（第row行）
        if row > n:
            # 找到一组完整解，只取1~n
            result.append(queen[1:].copy())
            return
        # 枚举第row行可选的列，从1到n
        for col in range(1, n + 1):
            d1 = row - col + n
            d2 = row + col
            # O(1) 判断是否冲突
            if not col_used[col] and not diag1[d1] and not diag2[d2]:
                # 放置皇后
                queen[row] = col
                col_used[col] = True
                diag1[d1] = True
                diag2[d2] = True

                backtrack(row + 1)

                # ✅ 回溯：撤销标记（恢复现场，这一步不能省！）
                col_used[col] = False
                diag1[d1] = False
                diag2[d2] = False

    backtrack(1)
    return result


def print_board(sol, n):
    """sol是[col1,col2,...coln]，依次为第1,2...n行皇后的列号，打印棋盘"""
    for r in range(1, n+1):
        line = ["."] * n
        c = sol[r-1] - 1   # 转成打印用0下标
        line[c] = "Q"
        print("".join(line))


if __name__ == "__main__":
    N = 4
    all_sols = solve_n_queens(N)
    print(f"N={N}，一共 {len(all_sols)} 组解\n")
    for idx, s in enumerate(all_sols, 1):
        print(f"===== 解{idx}：queen[1..{N}] = {s} =====")
        print_board(s, N)
        print()
