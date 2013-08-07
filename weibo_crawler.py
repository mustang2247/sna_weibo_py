#coding=utf-8
class User(object):
    """微博用户
    Attributes:
        url: 用户url
        uid: 用户id
        following_number: 用户关注数 
        follower_number: 用户粉丝数
        sex: 性别
        age: 年龄
        tags: 标签
    """
    def __init__(self, url = None, uid = None, following_number = None,\
            follower_number = None, sex = None, age = None,\
            tags = None):
        self.url = url
        self.uid = uid
        self.following_number = following_number
        self.follower_number = follower_number
        self.sex = sex
        self.age = age
        self.tags = tags
    
class WeiboPost(object):
    """一条新浪微博。
    Attributes:
        mid: 字符串，微博的mid，形如zAjoQmY0n
        user: 字符串发布者
        post_time: 发布时间
        content: 字符串内容
        repost_list: WeiboReply回复列表
    """
    def __init__(self, mid=None, user=None, post_time=None, content=None):
        self.mid = mid
        self.user = user
        self.post_time = post_time
		self.content = content
class WeiboRepost:
    """一条微博回复。
    Attributes:
        content: 内容
        time: 时间
        user: 发布者
        from_user: 转发来源
    """
    def __init__(self, content=None, time=None, user=None, from_user=None):
        self.content = content
        self.time = time
        self.user = user
        self.from_user = from_user

def get_replies(url):
    """以list形式通过url取得一个页面内的回复。
    Args:
        url: 页面的链接字符串，包含page参数、gsid、mid等，形如：http://weibo.cn/repost/yci8hkTUf?&gsid=4uwgb764149TppfO8K622703C8g&page=2
    Returns: 
        一个list，其中的元素为WeiboReply类的实例
    """
    list = []
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"}
    request = urllib2.Request(url,headers=headers)
    data = urllib2.urlopen(request).read()
    dom = soupparser.fromstring(data)
    divs = dom.xpath("//*[@class='c']")
    for i in range(0,len(divs)):
        nodes  =  divs[i].xpath('node()')
        if len(nodes)==0:
            continue
        elif nodes[-1].tag!='span':
            continue
        weibo_reply = WeiboReply()
        full_url_string = "weibo.cn%s" % nodes[0].get('href')
        weibo_reply.user_url = full_url_string
        weibo_reply.user_url = re.compile(r'(\S*)?\?').match(full_url_string).group(1)
        print weibo_reply.user_url
        time_string = re.compile(ur'(.*)\u6765.*').match(nodes[-1].text).group(1).strip()
        print time_string
        time_string_split = time_string.split()
        match_ymd = re.compile(ur'(\d{4})-(\d{2})-(\d{2})').match(time_string_split[0])
        if len(time_string_split)==1:
            print "case1"
            minutes = re.compile(ur'(.*)\u5206.*').match(time_string_split[0]).group(1)    #取得转发距现在过去了几分钟
            #print minutes
            weibo_reply.repost_time = datetime.datetime.today()\
                    +datetime.timedelta(minutes = 0-int(minutes))

        elif u'\u4eca\u5929' in time_string_split:
            print "case2"
            time = time_string_split[1]    #取得转发时间HH:mm
            hour,minutes = time.split(":")
            today = datetime.date.today()
            weibo_reply.repost_time = datetime.datetime(today.year,\
                    today.month,\
                    today.day,\
                    int(hour),int(minutes))
        elif u'\u6708' in time_string_split[0] and u'\u65e5' in time_string_split[0]:
            print "case3"
            date_string = time_string_split[0]
            match = re.compile(ur'(\d{2}).*(\d{2}).*').match(date_string)
            today = datetime.date.today()
            month = match.group(1)
            day = match.group(2)
            time = time_string_split[1]
            hour,minutes = time.split(":")
            #print "nomth,day : %s, %s "% (month,day)
            weibo_reply.repost_time = datetime.datetime(today.year,\
                    int(month),\
                    int(day),\
                    int(hour),int(minutes))
        elif match_ymd!=None:
            print "case4"
            year = match_ymd.group(1)
            month = match_ymd.group(2)
            day = match_ymd.group(3)
            #print "year-month-day:%s,%s,%s"%(year,month,day)
            time = time_string_split[1]
            hour,minutes,_ = time.split(":")
            weibo_reply.repost_time = datetime.datetime(int(year),\
                    int(month),\
                    int(day),\
                    int(hour),int(minutes))
        print "repost_time : %s"%weibo_reply.repost_time
        list.append(weibo_reply)
    return list
    

