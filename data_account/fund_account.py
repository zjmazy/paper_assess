from numpy import nan
import pandas as pd
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
from collections import Counter

path = r'together.xls'

data = pd.read_excel(path, sheet_name = 'together')
fund = data['Fund-基金']
temp_fund = fund[:]
temp = []
num = 0

for i in range(len(fund)):
    if isinstance(fund[i], str):
        temp_split = fund[i].split(";; ")
        del temp_fund[i]
        temp += temp_split
        num = num + 1
    else:
        del temp_fund[i]
        num = num + 1

print(len(temp))
fund = temp

fund_result = Counter(fund).most_common(10)
print(fund_result)
x_data = []
y_data = []
for i in range(len(fund_result)):
    x_data.append(fund_result[i][0])
    y_data.append(fund_result[i][1])
# print(x_data)
# print(y_data)

#饼图用的数据格式是[(key1,value1),(key2,value2)]，所以先使用 zip函数将二者进行组合
data_pair = [list(z) for z in zip(x_data, y_data)]

pie = (
#初始化配置项，内部可设置颜色
    Pie(init_opts=opts.InitOpts(bg_color="#ffffff"))
    .add(
        #系列名称，即该饼图的名称
        series_name="基金来源分析",
        #系列数据项，格式为[(key1,value1),(key2,value2)]
        data_pair=data_pair,
        #通过半径区分数据大小 “radius” 和 “area” 两种
        rosetype="radius",
        #饼图的半径，设置成默认百分比，相对于容器高宽中较小的一项的一半
        radius="55%",
        #饼图的圆心，第一项是相对于容器的宽度，第二项是相对于容器的高度
        center=["50%", "50%"],
        #标签配置项
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .add(
        #系列名称，即该饼图的名称
        series_name="基金来源分析",
        #系列数据项，格式为[(key1,value1),(key2,value2)]
        data_pair=data_pair,
        #通过半径区分数据大小 “radius” 和 “area” 两种
        rosetype="radius",
        #饼图的半径，设置成默认百分比，相对于容器高宽中较小的一项的一半
        radius="55%",
        #饼图的圆心，第一项是相对于容器的宽度，第二项是相对于容器的高度
        center=["50%", "50%"],
        #标签配置项
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    #全局设置
    .set_global_opts(
        #设置标题
        title_opts=opts.TitleOpts(
            #名字
            title="论文基金来源分析",
            #组件距离容器左侧的位置
            pos_left="center",
            #组件距离容器上方的像素值
            pos_top="20",
            #设置标题颜色
            title_textstyle_opts=opts.TextStyleOpts(color="#000000"),
        ),
        #图例配置项，参数 是否显示图里组件
        legend_opts=opts.LegendOpts(is_show=False),
    )
    #系列设置
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}"
        ),
        #设置标签颜色
        label_opts=opts.LabelOpts(color="rgba(0, 0, 0, 0.5)"),
    )
)

pie.render('test.html')