#引入所需库
import requests
import csv
from lxml import html
import os
import re


#定义常量
BASE_URL="https://www.themoviedb.org"#TMDB网站主页面
HIGHSCORE="https://www.themoviedb.org/movie/top-rated"#高分电影榜单首页，top20
HIGHSCORE2="https://www.themoviedb.org/discover/movie/items"#高分榜第二页及之后的数据请求头
MOVIE="csv_file/All_movies.csv"

#对所得到的数据进行清洗
def m_show(movie_show_time):
    show_clean=movie_show_time[0].strip() if movie_show_time else ''
    r=re.search(r'\d{4}-\d{2}-\d{2}', show_clean)
    return r.group() if r else ''

def m_year(movie_year):
    year_clean=movie_year[0].strip() if movie_year else ''
    return year_clean.replace("(","").replace(")","")


def m_time(movie_last_time):
    time_clean=movie_last_time[0].strip() if movie_last_time else ''
    h_=re.search(r'(\d+)h',time_clean)
    m_=re.search(r'(\d+)m',time_clean)
    h=int(h_.group(1)) if h_ else 0
    m=int(m_.group(1)) if m_ else 0
    return h*60+m


def get_detail(movie_info_url):#获取详细信息
    response1=requests.get(movie_info_url,timeout=5)
    doc1=html.fromstring(response1.text)
    movie_name=doc1.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")
    movie_last_time=doc1.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[4]/text()")
    movie_rate=doc1.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")
    movie_year=doc1.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")
    movie_show_time=doc1.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[2]/text()")
    movie_lau=doc1.xpath("//*[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")
    movie_tag=doc1.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[3]/a/text()")

    #封装所有信息到字典
    all_info={
        "电影名称":movie_name[0].strip() if movie_name else '',
        "电影评分":movie_rate[0].strip() if movie_rate else '',
        "电影年份":m_year(movie_year),
        "上映时间":m_show(movie_show_time),
        "电影时长":m_time(movie_last_time),
        "电影语言":movie_lau[0].strip() if movie_lau else '',
        "电影标签":','.join(movie_tag) if movie_tag else '',
    }
    return all_info


def save_all_movies(all_move_list):
    os.makedirs('csv_file',exist_ok=True)#新建csv文件夹
    with open(MOVIE, 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["电影名称", "电影评分", "电影年份", "上映时间", "电影时长", "电影语言", "电影标签"])
        writer.writeheader()
        writer.writerows(all_move_list)


def strat():
    n=0#用于计数
    all_move_list = []  # 用于存储所有电影信息
    for page_num in range(1,6):#设置多页循环
        if page_num == 1:
            response = requests.get(HIGHSCORE, timeout=5)
        else:
            response = requests.post(HIGHSCORE2,
                                     f"air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-04-12&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&vote_count.lte=&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400&view=&discover_preset=top-rated",
                                     timeout=5)
        doc = html.fromstring(response.text)
        print(f"正在解析第{page_num}页网页信息...")
        movie_list = doc.xpath(f"//*[@id='page_{page_num}']/div/div/div")
        for movie in movie_list:
            movie_url = movie.xpath("./div/div/a/@href")  # 拿到对应电影详情页网址后缀
            if movie_url:
                movie_info_url = BASE_URL + movie_url[0]
                D = get_detail(movie_info_url)  # 得到电影详情信息
                n+=1
                print(f"已获取第{n}部电影信息")
                all_move_list.append(D)# 将信息添加到列表中
    print('正在将获取到的电影信息存入csv文件中...')
    save_all_movies(all_move_list) # 将获取的所有信息保存到csv文件中
    print("已成功完成所有电影信息的获取和保存！")


if __name__ == '__main__':
    strat()