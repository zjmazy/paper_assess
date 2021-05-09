from collections import Counter
from numpy import NaN, source
from pandas import DataFrame
import pandas as pd
import re
import random
import numpy as np

# 将excel单元格中含有多个元素的数据按照分割符号分割，如A；B分隔符为；，元素为A和B
def get_separate(data, separator):
    temp_data = data[:]
    temp = []
    num = 0

    for i in range(len(data)):
        if isinstance(data[i], str):
            temp_split = data[i].split(separator)
            del temp_data[i]
            if separator == ";; ":
                temp_split = delete_fund_sign(temp_split)
            temp += temp_split
            num = num + 1
        else:
            del temp_data[i]
            num = num + 1
    data = temp
    return data

# 基金的项目中含有基金编号，进行统计时应该用正则匹配去除，达到统计基金本体的目的
def delete_fund_sign(data):
    for i in range(len(data)):
        data[i] = re.sub('\(.*?\)', '', data[i])
        data[i] = re.sub('\（.*?\）', '', data[i])
        data[i] = re.sub('\（.*?\)', '', data[i])
        data[i] = re.sub('\(.*?\）', '', data[i])
    return data

# 数据预处理，进行指标的统计
def data_wash_account(data, separator):
    data = get_separate(data, separator)
    data_result = Counter(data).most_common()
    x_data = []
    y_data = []
    # 把对应的数据与频次写入x与y，注意要舍去缺省值
    for i in range(len(data_result)-1 if data_result[0][0]=='' else len(data_result)):
        if data_result[0][0] == '':
            x_data.append(data_result[i+1][0])
            y_data.append(data_result[i+1][1])
        else:
            x_data.append(data_result[i][0])
            y_data.append(data_result[i][1])
    return x_data, y_data

# 将处理好的数据写入excel
def write_into_excel(name, x, y, writer, title):
    if name == "fund":
        dict = {
            "论文标题": title,
            name: x,
            '基金等级': y
        }
    else:
        dict = {
            name: x,
            '出现频次': y
            }
    df = pd.DataFrame(dict)
    df.to_excel(writer, index=False, sheet_name=name)
    return 0

# 如果同一篇论文指标有多个元素，获得指标平均值
def get_average(data, x, y, length, separator):
    title_grade = []
    for i in range(length):
        grade = 0
        if isinstance(data[i], str):
            temp_data = data[i].split(separator)
            if temp_data[len(temp_data)-1] == '':
                del temp_data[len(temp_data)-1]
            if separator == ";; ":
                temp_data = delete_fund_sign(temp_data)
            for j in range(len(temp_data)):
                index = x.index(temp_data[j])
                grade += y[index]
            grade = grade / len(temp_data)
        else:
            temp_data = ['无']
        # print(str(temp_data) + "所获得分：" + str(grade))
        title_grade.append(grade)
    return title_grade

# 基金按照等级划分指标
def get_fund_grade(fund):
    fund_grade = [0 for _ in range(len(fund))]
    for i in range(len(fund)):
        if isinstance(fund[i], str):
            temp = fund[i].split(";; ")
            for j in range(len(temp)):
                if "国家" in temp[j]:
                    fund_grade[i] = fund_grade[i] + 5
                elif "中国" in temp[j]:
                    fund_grade[i] = fund_grade[i] + 5
                elif "全国" in temp[j]:
                    fund_grade[i] = fund_grade[i] + 5
                elif "教育部" in temp[j]:
                    fund_grade[i] = fund_grade[i] + 4
                elif "中央" in temp[j]:
                    fund_grade[i] = fund_grade[i] + 4
                elif "省" in temp[j]:
                    fund_grade[i] = fund_grade[i] + 3
                elif "市" in temp[j]:
                    fund_grade[i] = fund_grade[i] + 2
                elif "大学" in temp[j]:
                    fund_grade[i] = fund_grade[i] + 2
                else:
                    fund_grade[i] = fund_grade[i] + 1
        else:
            fund_grade[i] = 0
    return fund_grade

# 随机生成下载量数据
def get_download_data(data):
    downloads_data = []
    for i in range(len(data)):
        if np.isnan(data[i]):
            downloads_data.append(random.randint(800, 1000))
        else:
            downloads_data.append(int(data[i]))
    return downloads_data

# 随机生成文献数据
def get_source_data(len):
    source = ['《中国高教研究》', '《中国高等教育》', '《高等教育研究》', '《大学教育科学》', '《高等工程教育研究》', '《现代教育管理》', '《现代大学教育》', '《黑龙江高教研究》', '《高校发展与评估》', '《学位与研究生教育》', '《高教探索》', '《江苏高教》', '《复旦教育论坛》', '《中国大学教学》', '《教育发展研究》', '《北京大学教育评论》']
    return np.random.choice(source, len);