
# 微信好友分析

## 依赖
本程序使用python3，请在python3环境下运行

安装:
方法一:
  pip install -r requirements.txt

方法二:
- PIL: pip3 install pillow
- pyecharts：pip3 install pyecharts
- pip3 install itchat
- pip3 install jieba

地图数据包：
pip3 install echarts-china-provinces-pypkg
pip3 install echarts-countries-pypkg


#### 取微信好友信息
python3 get_user.py
执行后会在data目录下生成friends.json
会在images目录下存放所有好友的头像

#### 统计用户信息
python3 analyse.py
会在analyse文件夹下生产合成后的图片以及可视化的文件

to_mongo.py #向mongodb中存/取数据
settiong.py #连接mongodb需要的信息

参考来源:https://zhuanlan.zhihu.com/p/37621427


## 功能说明：

#### 1：统计好友的性别(饼图)
![python](https://github.com/srp527/MyWeChat/blob/master/images/%E6%80%A7%E5%88%AB%E7%BB%9F%E8%AE%A1%E5%9B%BE.png)
#### 2：统计好友的地域分布，并且可视化在地图上展示
![python](https://github.com/srp527/MyWeChat/blob/master/images/%E5%9C%B0%E5%8C%BA%E7%BB%9F%E8%AE%A1.png)

![python](https://github.com/srp527/MyWeChat/blob/master/images/%E5%BE%AE%E4%BF%A1%E5%A5%BD%E5%8F%8B%E5%9C%B0%E5%9B%BE%E5%88%86%E5%B8%83.png)
#### 3：将好友的昵称做成词云
因为这个信息比较私人，这里就不展示
#### 4：统计好友个性签名中的高频词汇
![python](https://github.com/srp527/MyWeChat/blob/master/images/%E5%BE%AE%E4%BF%A1%E5%A5%BD%E5%8F%8B%E7%AD%BE%E5%90%8D%E5%85%B3%E9%94%AE%E5%AD%97.png)
#### 5：将所有好友的头像合并成一张大图
![python](https://github.com/srp527/MyWeChat/blob/master/images/head_photo.png)


