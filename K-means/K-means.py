import random
from math import *
import matplotlib.pyplot as plt

# 从文件中读取数据


def read_data():
    data_points = []
    with open('data.txt', 'r') as fp:
        for line in fp:
            if line == '\n':
                continue
            # 去掉空格，并将data中的数据转化为tuple
            data_points.append(tuple(map(float, line.split(' '))))
        fp.close()
        return data_points

# 初始化聚类中心

def begin_cluster_center(data_points, k):
    center = []
    length = len(data_points)  # 计算长度
    rand_data = random.sample(range(0, length), k)  # 生成k个不同的随机数
    for i in range(k):  # 得到k个聚类中心(随机选出)
        center.append(data_points[rand_data[i]])
    return center

# 计算最短距离

def distance(a, b):
    length = len(a)
    sum = 0
    for i in range(length):
        sq = (a[i]-b[i])**2
        sum += sq
    return sqrt(sum)



# 分配样本
# 按照最短距离将所有样本分配到k个聚类中心的某一个

def assign_points(data_points, center, k):
    assignment = []
    for i in range(k):
        assignment.append([])
    for point in data_points:
        min = 10000000
        flag = -1
        for i in range(k):
            value = distance(point, center[i])
            if value < min:
                min = value
                flag = i
        assignment[flag].append(point)
    return assignment

# 更新聚类中心，计算每一簇中所有点的平均值

def update_cluster_center(center, assignment, k):
    for i in range(k):
        x = 0
        y = 0
        length = len(assignment[i])
        if length != 0:
            for j in range(length):
                x += assignment[i][j][0]
                y += assignment[i][j][1]
            center[i] = (x/length, y/length)
    return center


# 计算平方误差
def getE(assignment, center):
    sum_E = 0
    for i in range(len(assignment)):
        for j in range(len(assignment[i])):
            sum_E += distance(assignment[i][j],center[i])
    return sum_E


# 计算各个聚类中的新向量，更新距离，即每一类中每一维均值向量
# 然后在进行分配，比较前后两个聚类中心向量是否相等
# 若不相等就继续进行循环，否则就进入循环，进入下一步
def k_means(data_points, k):
    # 由于初始聚类中心是随机选择的，十分影响聚类结果，聚类就可能会出现较大误差的现象
    # 因此如果由初始聚类中心第一次分配后有结果为空，重新初始聚类中心，重新再聚合一遍，直到符合要求
    while 1:
        # 产生初始聚类中心
        begin_center = begin_cluster_center(data_points, k)
        # 第一次分配样本
        assignment = assign_points(data_points, begin_center, k)
        for i in range(k):
            if len(assignment[i]) == 0:
                continue
        break
    # 第一次的平方误差
    begin_sum_E = getE(assignment, begin_center)
    # 更新聚类中心
    end_center = update_cluster_center(begin_center, assignment, k)
    # 第二次分配样本
    assignment = assign_points(data_points, end_center, k)
    # 第二次平方误差
    end_sum_E = getE(assignment, end_center)
    count = 2  # 计算器
    # 比较两个聚类中心向量是否相等
    while(begin_sum_E != end_sum_E):
        begin_center = end_center
        begin_sum_E = end_sum_E
        # 再次更新聚类中心
        end_center = update_cluster_center(begin_center, assignment, k)
        # 进行分配
        assignment = assign_points(data_points, end_center,k)
        # 计算误差
        end_sum_E = getE(assignment, end_center)
        count = count+1  # 计数器加1
    return assignment, end_sum_E, end_center, count

# 打最终聚类结果


def print_result(count, end_sum_E, k, assignment):
    print('经过', count, '次聚类，平方误差为：', end_sum_E)
    print('————————————————————分类结果————————————————————')
    for i in range(k):
        print('第', i+1, '类数据：', assignment[i])
    print('————————————————————————————————————————————————')

# 初始坐标列表’


def plot(k, assignment, center):
    x = []
    y = []
    for i in range(k):
        x.append([])
        y.append([])
    # 填充坐标 并绘制散点图
    for j in range(k):
        for i in range(len(assignment[j])):
            x[j].append(assignment[j][i][0])  # 横坐标填充
        for i in range(len(assignment[j])):
            y[j].append(assignment[j][i][1])
        plt.scatter(x[j], y[j], marker='o')
        plt.scatter(center[j][0], center[j][1], c='b', marker='*')
    # 设置标题
    plt.title('K-means Scatter Diagram')
    # 设置x轴标签
    plt.xlabel('X')
    # 设置y轴标签
    plt.ylabel('Y')
    # 显示散点图
    plt.show()


def main():
    #4个聚类中心
    k = 4
    data_points = read_data()
    assignment, end_sum_E, end_center, count = k_means(data_points, k)
    min_sum_E = 1000
# 返回较小误差
    while min_sum_E > end_sum_E:
        min_sum_E = end_sum_E
        assignment, end_sum_E, end_center, count = k_means(data_points, k)
    print_result(count, min_sum_E, k, assignment)  # 输出结果
    plot(k, assignment, end_center)  # 画图


main()
