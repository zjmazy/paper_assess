import numpy as np
import random

#一个最简单的KNN
class KMeans():
    
    def __init__(self, k=2):
        self.model = {}#存储各个类别的训练样本的特征，key为类别标签，value是一个list，元素为样本的特征向量
        self.K = k#类别的数量
    
    #训练模型。为了操作简单，输入数据是一个Map，key是样本id，value是对应的特征
    def fit(self, data_map, max_epoch=20):
        init_cluster_centers = self.generate_init_cluster_centers(data_map)
        print("init_cluster_centers", init_cluster_centers)
        cluster_info = {}
        for id in data_map:
            cluster_info[id] = {"feature": data_map[id], "cluster_label": self.find_nearest_cluster_center(data_map[id], init_cluster_centers)}
        cluster_centers = init_cluster_centers
        for epoch in range(max_epoch):
            cluster_list = [[] for _ in cluster_centers]
            for id in cluster_info:
                cluster_list[cluster_info[id]['cluster_label']].append(cluster_info[id]['feature'])
            new_cluster_centers = []
            for cluster in cluster_list:
                new_center = np.mean(np.array(cluster), axis=0)#求这个簇里的所有样本的质心，也可以理解为“中心位置”
                new_cluster_centers.append(new_center)
            print(epoch, new_cluster_centers)
            for id in data_map:
                cluster_info[id] = {"feature": data_map[id], "cluster_label": self.find_nearest_cluster_center(data_map[id], new_cluster_centers)}
                
        self.model = new_cluster_centers
        print("聚类结果是", list(map(lambda x: [x[0], x[1]['cluster_label']], cluster_info.items())))
        print("各个簇的中心是", new_cluster_centers)
     
    #聚类算法的使用，有两个阶段:(1)对一堆数据进行无监督分类:(2)基于训练得到的簇中心，构建一个kNN分类器，进行分类
    #无监督分类过程中，基于簇中心判断样本类别
    def find_nearest_cluster_center(self, x, center_feature_list):
        label = None#类别标签
        min_d = None#目前为止，待分类样本与各类代表性样本的最小平均距离
        for class_label in range(len(center_feature_list)):#遍历每个类别的代表性样本
            print(x, center_feature_list[class_label])
            dist = self.distance(x, center_feature_list[class_label])#累计
            print("dist", dist)
            if min_d==None or dist<=min_d:#如果遍历到第一个类别，或者待分类样本与当前类别的平均距离比之前的更低，更新类标签与最小距离
                label = class_label
                min_d = dist
        return label
    
    def generate_init_cluster_centers(self, data_map):
        init_cluster_centers = list(data_map.keys())
        random.shuffle(init_cluster_centers)
        cluster_centers = [data_map[id] for id in init_cluster_centers[:self.K]]
        return cluster_centers
        
    #knn分类器阶段，对单个样本分类
    def predict(self, x):
        label = None#类别标签
        min_d = None#目前为止，待分类样本与各类代表性样本的最小平均距离
        for class_label in range(len(self.model)):#遍历每个类别的代表性样本
            print(x, self.model[class_label])
            dist = self.distance(x, self.model[class_label])#累计
            print("dist", dist)
            if min_d==None or dist<=min_d:#如果遍历到第一个类别，或者待分类样本与当前类别的平均距离比之前的更低，更新类标签与最小距离
                label = class_label
                min_d = dist
        return label
    

    
    #计算两个样本之间的距离
    def distance(self, x1, x2, type="eu"):
        d= None
        if type=="eu": d = np.sum((x1-x2)**2)#欧氏距离
        return d
    
    #制造训练数据
    def generate_training_data(self):
        data_str = """id f1 f2
赵本山    170    70
我    178    75
大熊猫盼盼    100    100
金丝猴孙悟空    120    40
老鼠舒克    10    0.1"""
        print(data_str)
        data_list = data_str.split('\n')
        data_map = {}
        for line in data_list[1:]:
            data = line.split("    ")
            data_map[data[0]] = np.array(list(map(lambda x: float(x), data[1:])))
        return data_map

if __name__ == '__main__':
    M = KMeans()
    data_map = M.generate_training_data()
    M.fit(data_map)
    res = M.predict(np.array([166, 45]))
    print(res)