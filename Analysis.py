import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts.charts import Map

def main():
    path = r'data/BossData.xls'
    data = readFile(path)
    draw(data)


def readFile(path):
    df = pd.DataFrame(pd.read_excel(path))
    return df


#北京市大数据岗位平均薪资
def draw(data):
    average_salary = data.groupby('工作位置')['平均薪资水平'].mean()  # 平均工资
    average_low_salary = data.groupby('工作位置')['最小薪资水平'].mean()  # 最低平均工资
    average_high_salary = data.groupby('工作位置')['最大薪资水平'].mean()  # 最高平均工资
    average_year_salary = data.groupby('工作位置')['年薪'].mean()  # 年薪
    x = average_salary.reset_index()['工作位置'].tolist()
    y1 = average_salary.reset_index()['平均薪资水平'].tolist()
    y2 = average_low_salary.reset_index()['最小薪资水平'].tolist()
    y3 = average_high_salary.reset_index()['最大薪资水平'].tolist()
    y4 = average_year_salary.reset_index()['年薪'].tolist()

    # 保留一位小数
    for j in [y1,y2,y3,y4]:
        for i in range(len(j)):
            j[i] = round(j[i],1)

    # print(x)
    # print(y1)
    # print(y2)
    # print(y3)


    bar = Bar()
    bar.set_global_opts(title_opts=opts.TitleOpts(title="北京市大数据岗位平均薪资", subtitle="单位:千(K)"))
    bar.add_xaxis(x)
    bar.add_yaxis("平均薪资水平", y1)
    bar.add_yaxis("平均最小薪资水平", y2)
    bar.add_yaxis("平均最大薪资水平", y3)
    bar.render('res/各城市工资.html')

    bar1 = Bar()
    bar1.add_xaxis(x)
    bar1.set_global_opts(title_opts=opts.TitleOpts(title="北京市大数据岗位平均年薪", subtitle="单位:千(K)"))
    bar1.add_yaxis("平均年薪", y4)
    bar1.render('res/平均年薪.html')

    #各区域工作数量
    jobSum = data.groupby('工作位置').count()
    jobSum = jobSum.reset_index()['岗位'].tolist()
    # print(jobSum)
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(x, jobSum)],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各区域工作数量"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("res/各区域工作数量.html")
    )

    #各学历工资状况
    job_education_average_salary = data.groupby('要求学历')['平均薪资水平'].mean()  # 平均工资
    job_education_average_low_salary = data.groupby('要求学历')['最小薪资水平'].mean()  # 最低平均工资
    job_education_average_high_salary = data.groupby('要求学历')['最大薪资水平'].mean()  # 最高平均工资
    x = job_education_average_salary.reset_index()['要求学历'].tolist()
    y1 = job_education_average_salary.reset_index()['平均薪资水平'].tolist()
    y2 = job_education_average_low_salary.reset_index()['最小薪资水平'].tolist()
    y3 = job_education_average_high_salary.reset_index()['最大薪资水平'].tolist()

    bar = Bar()
    bar.add_xaxis(x)
    bar.add_yaxis("平均薪资水平", y1)
    bar.add_yaxis("平均最小薪资水平", y2)
    bar.add_yaxis("平均最大薪资水平", y3)

    for j in [y1,y2,y3]:
        for i in range(len(j)):
            j[i] = round(j[i],1)
    # 导出绘图html文件，可直接用浏览器打开
    bar.render('res/各学历工资状况.html')

    # 各学历要求数量
    degree = data.groupby('要求学历').mean()  # 平均工资
    degree = degree.reset_index()['要求学历'].tolist()
    print(degree)
    degreeSum = data.groupby('要求学历').count()
    degreeSum = degreeSum.reset_index()['岗位'].tolist()
    print(degreeSum)
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(degree, degreeSum)],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各区域工作数量"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("res/要求学历数量.html")
    )

    #大数据岗位词云
    job = data.groupby('岗位')['公司'].count()
    jobsum = job.tolist()
    job = job.reset_index()['岗位'].tolist()

    words = []
    for i in range(len(job)):
        content = (job[i],jobsum[i])
        words.append(content)
    print(len(words))

    (
        WordCloud()
            .add(series_name="大数据岗位词云", data_pair=words, word_size_range=[15, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="大数据岗位词云", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
            .render("res/大数据岗位词云.html")
    )

    #北京地区图
    area = data.groupby('工作位置')['公司'].count()
    areasum = area.tolist()
    area = area.reset_index()['工作位置'].tolist()

    # words = []
    # for i in range(len(area)):
    #     content = (area[i], areasum[i])
    #     words.append(content)
    # print(words)

    c = (
        Map()
            .add("", [list(z) for z in zip(area, areasum)], "北京")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="大数据岗位地区分布"), visualmap_opts=opts.VisualMapOpts()
        )
            .render("res/大数据岗位地区分布.html")
    )

if __name__ == '__main__':
    main()