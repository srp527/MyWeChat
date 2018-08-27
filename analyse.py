# -*- coding:utf-8 -*- 
__author__ = 'SRP'

import json
import re
import os
import math

from pyecharts import Bar,Grid,WordCloud,Pie,Map
from collections import Counter
import jieba.analyse
import PIL.Image as Image
import codecs

from to_mongo import MongoPipeline as db

def get_pie(title,name_list,num_list):
    '''生成性别比例饼图'''

    friend_nums = num_list[0] + num_list[1] + num_list[2]
    subtitle = '共有:%d个好友' %friend_nums

    pie = Pie(title,page_title=title,title_text_size=30,title_pos='center',
              subtitle=subtitle,subtitle_text_size=25,width=800,height=800)
    pie.add("",name_list,num_list,is_label_show=True,center=[50,45],radius=[0,50],
            legend_pos='right',legend_orient='vertical',label_text_size=20)

    out_file_name = './analyse/'+ title + '.html'
    pie.render(out_file_name)

def get_bar(title,name_list,num_list):
    '''地区统计条形图'''

    bar = Bar(title,page_title=title,title_text_size=30,title_pos='center')

    bar.add("",name_list,num_list,title_pos='center',xaxis_interval=0,xaxis_rotate=27,
            xaxis_label_textcolor=20,yaxis_label_textcolor=20,yaxis_name_pos='end',yaxis_pos="%50")
    bar.show_config()

    grid = Grid(width=1300,height=800)
    grid.add(bar,grid_top='13%',grid_bottom='23%',grid_left='15%',grid_right='15%')
    out_file_name = './analyse/'+title+'.html'
    grid.render(out_file_name)


def get_map(title,name_list,num_list):
    '''区域分布图'''

    # print('---->>',name_list,num_list)
    _map = Map(title,width=1300,height=800,title_pos='center',title_text_size=30)
    _map.add("",name_list,num_list,maptype='china',is_visualmap=True,visual_text_color='#000')

    out_file_name = './analyse/'+title+'.html'
    _map.render(out_file_name)


def word_clout(title,name_list,num_list,word_size_range):
    '''词云图'''

    wordcloud = WordCloud(width=1400,height=900)

    wordcloud.add("",name_list,num_list,word_size_range=word_size_range,shape='pentagon')
    out_file_name = './analyse/'+title+'.html'
    wordcloud.render(out_file_name)


def get_item_list(first_item_name,dict_list):
    item_name_list = []
    item_num_list = []
    i = 0
    for item in dict_list:
        i+=1
        if i >= 15:
            break
        for name,num in item.items():
            if name != first_item_name:
                item_name_list.append(name)
                item_num_list.append(num)
    return item_name_list,item_num_list


def dict2list(_dict):
    name_list = []
    num_list = []

    for k,v in _dict.items():
        name_list.append(k)
        num_list.append(v)
    return name_list,num_list


def counter2list(_counter):
    name_list = []
    num_list = []

    for item in _counter:
        name_list.append(item[0])
        num_list.append(item[1])
    return name_list,num_list


def get_tag(text,cnt):
    text = re.sub(r'<span.*><span>','',text)
    print('正在分析句子:',text)
    tag_list = jieba.analyse.extract_tags(text)
    for tag in tag_list:
        cnt[tag] += 1


def mergeImage():
    '''头像合成'''

    print('正在合成头像图')
    photo_width = 50
    photo_height = 50

    photo_path_list = []  #头像路径

    dirName = os.getcwd()+'/images' #获取当前路径

    #遍历文件夹获取所有图片路径
    for root,dirs,files in os.walk(dirName):
        for file in files:
            if 'jpg' in file and os.path.getsize(os.path.join(root,file)) > 0:
                photo_path_list.append(os.path.join(root,file))
            elif 'jpg' in file and os.path.getsize(os.path.join(root,file)) == 0:
                photo_path_list.append(os.path.join('./source','empty.jpg'))

    pic_num = len(photo_path_list)

    line_max = int(math.sqrt(pic_num))-2
    row_max = int(math.sqrt(pic_num))+4
    print(line_max,row_max,pic_num)

    if line_max > 20:
        line_max = 20
        row_max = 20
    num = 0
    pic_max = line_max*row_max
    toImage = Image.new('RGBA',(photo_width*line_max,photo_height*row_max))

    for i in range(0,row_max):
        for j in range(0,line_max):
            pic_fole_head = Image.open(photo_path_list[num])
            # width,height = pic_fole_head.size

            #将图片压缩成设定大小
            tmppic = pic_fole_head.resize((photo_width,photo_height))

            loc = (int(j%line_max*photo_width),int(i%row_max*photo_height))
            toImage.paste(tmppic,loc)
            num += 1
            if num >= len(photo_path_list):
                break
        if num >= pic_max:
            break
    print(toImage.size)
    toImage.save('./analyse/head_photo.png')


if __name__ == '__main__':

    #读取文件中的数据
    # friends_file = './data/friends.json'
    # with codecs.open(friends_file,encoding='utf-8') as f:
    #     friends = json.load(f)

    #读取mongodb中的数据
    mongodb = db()
    friends_info = mongodb.from_mongo()
    mongodb.close_mongo()
    friends = list(friends_info)

    # 待统计参数
    sex_counter = Counter()       #性别
    Province_counter = Counter()  #省份
    Signature_counter = Counter() #个性签名
    NickName_list = []

    for friend in friends:
        sex_counter[friend['Sex']] += 1

        #将非中文地址换成空
        friend['Province'] = re.sub('[a-zA-Z]','',friend['Province']).strip()

        if friend['Province'] != '':
            Province_counter[friend['Province']] += 1

        #昵称
        NickName_list.append(friend['NickName'])
        # 签名关键词提取
        # get_tag(friend['Signature'],Signature_counter)

    ##性别饼图
    name_list,num_list = dict2list(sex_counter)
    # get_pie('性别统计图',name_list,num_list)

    #省份条形图 前15
    name_list,num_list = counter2list(Province_counter.most_common(15))
    # get_bar('地区统计',name_list,num_list)

    #地图
    print('---->',name_list,num_list)
    # get_map('微信好友地图分布',name_list,num_list)

    #昵称
    num_list = [5 for i in range(1,len(NickName_list)+1)]
    # word_clout('微信好友昵称',NickName_list,num_list,[18,18])

    #签名关键字
    name_list,num_list = counter2list(Signature_counter.most_common(200))
    # word_clout('微信好友签名关键字',name_list,num_list,[20,100])

    #合成头像
    # mergeImage()












