经典算法实现
1 nqueen.py  基于回溯法实现了n皇后问题
2 backtrac_tsp.py 基于回溯法求解tsp问题，其中，generate_init_solution.py产生初始解，里面包含2个算法，一个是greedy1贪心算法，逐步加入最小距离的邻居，避免回路；另一个是random随机算法； load_tsp_file.py将data\\tsp\\目录下的某个文件转成实例名称、节点个数以及邻接矩阵。其中： data_preprocessing目录下放着原始数据，包括：
    ALL_tsp: 所有的tsp数据, ALL_tsp.tar.gz是其原始压缩文件；
    EUC2D.xlsx：是ALL_tsp中的利用二维欧几里得距离计算的实例情况说明
    tsp_instances.csv：是ALL_tsp中的所有的实例情况说明
    tsp95.pdf是说明文件
    原始网站：https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
    