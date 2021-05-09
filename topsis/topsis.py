import pandas as pd
import numpy as np


# 极小型指标：期望指标值越小越好（如患病率、死亡率等）
def dataDirection_1(datas, offset=0):
    def normalization(data):
	    return 1 / (data + offset)
    return list(map(normalization, datas))

# 中间型指标：期望指标值既不要太大也不要太小，适当取中间值最好（如水质量评估 PH 值）
def dataDirection_2(datas, x_min, x_max):
    def normalization(data):
        if data <= x_min or data >= x_max:
            return 0
        elif data > x_min and data < (x_min + x_max) / 2:
            return 2 * (data - x_min) / (x_max - x_min)
        elif data < x_max and data >= (x_min + x_max) / 2:
            return 2 * (x_max - data) / (x_max - x_min)
    return list(map(normalization, datas))

# 区间型指标：期望指标的取值最好落在某一个确定的区间最好（如体温）
def dataDirection_3(datas, x_min, x_max, x_minimum, x_maximum):
	def normalization(data):
		if data >= x_min and data <= x_max:
			return 1
		elif data <= x_minimum or data >= x_maximum:
			return 0
		elif data > x_max and data < x_maximum:
			return 1 - (data - x_max) / (x_maximum - x_max)
		elif data < x_min and data > x_minimum:
			return 1 - (x_min - data) / (x_min - x_minimum)
	return list(map(normalization, datas))

# 熵权法确定权重
def entropyWeight(data):
    data = np.array(data)
	# 归一化
    P = data / data.sum(axis=0)
	# 计算熵值，epsilon防止log中的数值过小出现警告
    epsilon = 1e-5
    E = np.nansum(-P * np.log(P + epsilon) / np.log(len(data) + epsilon), axis=0)
	# 计算权系数
    return (1 - E) / (1 - E).sum()

# topsis算法程序：需要输入原始数据和权系数（权系数默认使用熵权法定权. 也可以传入指定权重列表）
def topsis(data, weight=None):
	# 归一化
	data = data / np.sqrt((data ** 2).sum())

	# 最优最劣方案
	Z = pd.DataFrame([data.min(), data.max()], index=['负理想解', '正理想解'])

	# 距离
	weight = entropyWeight(data) if weight is None else np.array(weight)
	Result = data.copy()
	Result['正理想解'] = np.sqrt(((data - Z.loc['正理想解']) ** 2 * weight).sum(axis=1))
	Result['负理想解'] = np.sqrt(((data - Z.loc['负理想解']) ** 2 * weight).sum(axis=1))

	# 综合得分指数
	Result['综合得分指数'] = Result['负理想解'] / (Result['负理想解'] + Result['正理想解'])
	Result['排序'] = Result.rank(ascending=False)['综合得分指数']

	return Result, Z, weight