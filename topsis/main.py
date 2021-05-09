import pandas as pd
import data_process as dp
import topsis as tp
import numpy as np

if __name__ == '__main__':
    path = r'together.xlsx'

    excel_data = pd.read_excel(path, sheet_name = 'together')
    title = excel_data['Title-题名']
    author = excel_data['Author-作者']
    organ = excel_data['Organ-单位']
    fund = excel_data['Fund-基金']
    downloads = excel_data['Downloads-下载量']

    # 统计作者和机构出现的次数
    author_x, author_y = dp.data_wash_account(author, ";")
    organ_x, organ_y = dp.data_wash_account(organ, ";")
    # fund_x, fund_y = dp.data_wash_account(fund, ";; ")

    # 取得每篇论文各个指标的得分
    title_author = dp.get_average(author, author_x, author_y, len(title), ";")
    title_organ = dp.get_average(organ, organ_x, organ_y, len(title), ";")
    # title_fund = dp.get_average(fund, fund_x, fund_y, len(title), ";; ")
    title_fund = dp.get_fund_grade(fund)
    title_downloads = dp.get_download_data(downloads)
    
    # 将各数据出现的频次与得分存入account_data.xlsx表格中
    writer = pd.ExcelWriter('account_data.xlsx')
    dp.write_into_excel("author", author_x, author_y, writer, title)
    dp.write_into_excel("organ", organ_x, organ_y, writer, title)
    dp.write_into_excel("fund", fund, title_fund, writer, title)
    dp.write_into_excel("downloads", title, title_downloads, writer, title)
    writer.save()

    data = pd.DataFrame(
        {'作者发文数': title_author, '单位发文数': title_organ, '基金等级': title_fund, '论文下载量': title_downloads,
        }, index = title)

    # data['基金等级'] = tp.dataDirection_3(data['基金等级'], 1, 10, min(data['基金等级']), max(data['基金等级']))   # 基金等级数据为区间型指标
    # data['逾期毕业率'] = 1 / data['逾期毕业率']   # 逾期毕业率为极小型指标

    # 通过熵权法获得权值，并且使用topsis模型进行分析
    out = tp.topsis(data, None)
    # out = topsis(data, weight=[0.2, 0.3, 0.4, 0.1])    # 设置权系数

    out[0].insert(0, '文献来源', dp.get_source_data(len(title)))

    # 将建模结果输出到result.xlsx
    writer = pd.ExcelWriter('result.xlsx')
    out[0].to_excel(writer, sheet_name="归一化表与排名")
    out[1].to_excel(writer, sheet_name="最优方案与最劣方案")
    df_weight = pd.DataFrame(out[2], index=['作者发文数', '单位发文数', '基金等级', '论文下载量'], columns=['熵权法所得权重'])
    df_weight.to_excel(writer, sheet_name="熵权法获得的权重表")
    writer.save()
