import re
import sqlite3

import requests
import xlwt
from bs4 import BeautifulSoup


def main():
    baseurl = "https://www.zhipin.com/c101010100/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&page="
    savepath = r'BossData.xls'
    # getDataFromWeb(baseurl)
    basehtml = r'src\bossHtml'

    datalist = getDataFromLocalHTML(basehtml)
    # saveData(datalist, savepath)

    dbpath=r"BossData.db"
    saveDataToDB(datalist,dbpath)
    # test(datalist)



getName = re.compile(r'<span class="job-name">.*title="(.*)".*</span>')

getInkName = re.compile(r'<h3 class="name"><a href=".*" ka=".*" target="_blank" title=".*">(.*)</a></h3>')

getDegree = re.compile(r'<p>.*<em class="vline"></em>(.*)</p>')

getJobArea = re.compile(r'<span class="job-area">.*·(.*)·.*</span>')

getSalaryMin = re.compile(r'<span class="red">(.*)-.*</span>')
getSalaryMax = re.compile(r'<span class="red">.*-(.*)K.*</span>')
getSalaryTime = re.compile(r'<span class="red">.*-.*K·(.*)薪</span>')

getSkill = re.compile(r'<span class="tag-item">(.*)</span>')

# def getDataFromWeb(baseurl):
#     print("getdata running")
#     datalist = []
#
#     for i in range(0, 1):
#         url = baseurl + str(i)
#         html = getHTML(url)
#         print(html)
        # soup = BeautifulSoup(html, "html.parser")
        # for item in soup.find_all('div', class_="job-primary"):  # 查找符合要求的字符串形成类别
        #     data = []  # 保存一部电影的所有信息
        #     item = str(item)
        #
        #     jobArea = re.findall(getJobArea, item)
        #     print(jobArea)


def getDataFromLocalHTML(basehtml):
    datalist = []

    for i in range(1,9):
        htmlpath = basehtml + str(i) + '.html'
        # print(htmlpath)
        soup = BeautifulSoup(open(htmlpath, encoding='utf-8'),
                             features='html.parser')

        for item in soup.find_all('div', class_="job-primary"):
            data = []
            item = str(item)

            #工作名
            name = re.findall(getName, item)[0]
            data.append(name)

            #公司名
            inkName = re.findall(getInkName, item)
            if len(inkName) > 0:
                data.append(inkName[0])
            else:
                continue

            #工作区域
            jobArea = re.findall(getJobArea, item)
            # if len(jobArea) > 0:
            #     data.append(jobArea)
            # else:
            #     data.append("未知")
            if len(jobArea) == 0:
                continue
            else:
                data.append(jobArea[0])

            #薪水水平
            #最小薪资
            salaryMin = re.findall(getSalaryMin, item)[0]
            data.append(salaryMin)
            #最大薪资
            salaryMax = re.findall(getSalaryMax, item)[0]
            data.append(salaryMax)
            #平均薪资
            salaryMean = str((int(salaryMin) + int(salaryMax))/2)
            data.append(salaryMean)
            #每年薪资发放次数
            salaryTime = re.findall(getSalaryTime, item)
            # print(salaryTime)
            if len(salaryTime) > 0:
                data.append(salaryTime[0])
                yearSalary = str(float(salaryTime[0])*float(salaryMean))
            else:
                data.append("12")
                yearSalary = str(float(salaryMean) * 12)
            #以平均薪资计算的年薪水平
            data.append(yearSalary)


            # 要求学历
            degree = re.findall(getDegree, item)[0]
            data.append(degree)

            # 相关技能
            # skill = re.findall(getSkill, item)
            # data.append(skill)

            datalist.append(data)
    print(datalist)
    print(len(datalist))
    return datalist


def getHTML():
    url = 'https://www.zhipin.com/c101010100/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&page=2'
    headers = {
        "cookie": "lastCity=101010100; Hm_lvt_194df3105ad7148sdcf2b98a91b5e727a=1622099052,1622159897; __g=-; wt2=Ds3rGoRWHHHRVxnd1fflowUucoVdVEjUqZjU_tvz5OgkHoCkwqj_simGkxh_7Cl-rETia6XWaB5PqUwy4_avFYg~~; __l=l=/www.zhipin.com/web/geek/recommend?random=1622159973505&s=3&friend_source=0; _bl_uid=egkOhpbq7O4kn45swztvlRkrgzR4; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1622161915; __c=1622159898; __a=95786245.1622099052.1622099052.1622159898.15.2.7.15; __zp_stoken__=80ddcEE1ybAMbIiBLfkhmWTZcT1oYKWlUaEFBSgVSGV1KQXpyTUg4JxpITU0/YA15BXZNcWp/DxwTdjlmDFlvKjBtcEJMK2AHC1YOEVgQbFYlNwM6QRpRJG4hJwldJ0IENVVdTGwkBjdvYAVG; geek_zp_token=V1RNsiGeX_3V1rVtRvzR8ZLym06TzezC4~",
        "referer": "https://www.zhipin.com/c101010100/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&page=2",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    }

    params = {"query": "大数据",
              "page": "2",
              "ka": "page-2"}
    response = requests.get(url=url, headers=headers, params=params)
    html = response.text
    print(html)
    return html

def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('boss直聘', cell_overwrite_ok=True)
    col = ('岗位', '公司', '工作位置', '最小薪资水平','最大薪资水平','平均薪资水平','每年工资发放次数','年薪','要求学历','需要掌握的技能')
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    for i in range(0, len(datalist)):
        data = datalist[i]
        for j in range(0, len(col)):
            sheet.write(i + 1, j, data[j])

    book.save(savepath)


def init_db(dbpath):
    sql = '''
        create table BossData(
            id integer primary key autoincrement,
            job_name varchar,
            job_ink varchar,
            job_area varchar,
            job_low_salary numeric,
            job_max_salary numeric,
            job_avg_salary numeric,
            job_salary_times numeric,
            job_year_salary numeric,
            job_degree varchar
        )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def saveDataToDB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            data[index] = '"'+data[index]+'"'

        content = ",".join(data)

        sql = '''
            insert into BossData(
            job_name,job_ink,job_area,job_low_salary,job_max_salary,job_avg_salary,job_salary_times,job_year_salary,job_degree
            )
            values(%s)
        '''%content
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def test(datalist):
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
        content = ",".join(data)
        print(content)




if __name__ == '__main__':
    main()
    # init_db("BossData.db")
