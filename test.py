from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker

if __name__ == '__main__':

    c = (
        Map()
        .add("商家A", [list(z) for z in zip(Faker.provinces, Faker.values())], "北京")
        .set_global_opts(title_opts=opts.TitleOpts(title="Map-基本示例"))
        .render("map_base.html")
    )