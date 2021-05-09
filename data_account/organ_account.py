#导入的工具包
import pandas as pd
from pyecharts.charts import Bar, Pie, Page, Grid
from pyecharts import options as opts
from collections import Counter

from pyecharts.options.global_options import DataZoomOpts, InitOpts

Theme = 'Organ-单位'
except_organ = ['中国高等教育','中国高教研究','学位与研究生教育','高等教育研究','高等工程教育研究']
page = Page()

#Excel文件的地址
path = r'together.xls'

#读取Excel文件中theme的信息
data = pd.read_excel(path, sheet_name = 'together')
theme = data[Theme]

temp_theme = theme[:]
temp = []
num = 0

#按照；切片
for i in range(len(theme)):
    if isinstance(theme[i], str):
        temp_split = theme[i].split(";")
        del temp_theme[i]
        temp += temp_split
        num = num + 1
    else:
        del temp_theme[i]
        num = num + 1

print(len(temp))
theme = temp

#获取theme项目中出现次数最多的前6项（因为出现次数最多的为缺省，所以要舍去）
theme_result = Counter(theme).most_common(10)

x_data = []
y_data = []
#把theme和对应出现的次数从元祖中拆分出来，x为theme，y为次数
for i in range(len(theme_result)-1):
    if theme_result[i+1][0] in except_organ:
        num = num
    else:
        x_data.append(theme_result[i+1][0])
        y_data.append(theme_result[i+1][1])
# print(x_data)
# print(y_data)

#饼图用的数据格式是[(key1,value1),(key2,value2)]，所以先使用 zip函数将二者进行组合
data_pair = [list(z) for z in zip(x_data, y_data)]

pie = (
#初始化配置项，内部可设置颜色
    Pie()
    .add(
        #系列名称，即该饼图的名称
        series_name= Theme + "分析",
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
            title=Theme + "分析",
            #组件距离容器左侧的位置
            pos_left="center",
            #组件距离容器上方的像素值
            pos_top="20",
            #设置标题颜色
            title_textstyle_opts=opts.TextStyleOpts(color="#2c343c"),
        ),
        #图例配置项，参数 是否显示图里组件
        legend_opts=opts.LegendOpts(is_show=True),
    )
    #系列设置
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        #设置标签颜色
        label_opts=opts.LabelOpts(color="rgba(0, 0, 0, 0.6)"),
    )
)
page.add(pie)

#获取theme项目中出现次数最多的前6项（因为出现次数最多的为缺省，所以要舍去）
theme_result = Counter(theme).most_common(20)

x_data = []
y_data = []
#把theme和对应出现的次数从元祖中拆分出来，x为theme，y为次数
for i in range(len(theme_result)-1):
    if theme_result[i+1][0] in except_organ:
        num = num
    else:
        x_data.append(theme_result[i+1][0])
        y_data.append(theme_result[i+1][1])
# print(x_data)
# print(y_data)


bar=(
    Bar(init_opts=opts.InitOpts(height="1000px"))
    .add_xaxis(x_data)
    .add_yaxis("机构来源", y_data)
    # .reversal_axis()
    #全局设置
    .set_global_opts(
        #设置标题
        title_opts=opts.TitleOpts(
            #名字
            title=Theme + "分析",
            #组件距离容器左侧的位置
            pos_left="center",
            #组件距离容器上方的像素值
            pos_top="30",
            #设置标题颜色
            title_textstyle_opts=opts.TextStyleOpts(color="#2c343c"),
        ),
        # datazoom_opts=opts.DataZoomOpts(pos_bottom=50),
        #底部文字45°
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
        #图例配置项，参数 是否显示图里组件
        legend_opts=opts.LegendOpts(is_show=True),
    )
    #系列设置
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c}"
        ),
        #设置标签颜色
        label_opts=opts.LabelOpts(color="rgba(0, 0, 0, 0.6)"),
    )
)

grid=Grid()
# 可以分别调整上下左右的位置，可以是百分比，也可以是具体像素，如pos_top="50px"
grid.add(bar, grid_opts=opts.GridOpts(pos_bottom="30%", pos_left="15%"))

page.add(grid)

page.render(Theme + '.html')