class Weibo:
    def __init__(self):
        self.id = ''
        self.user_id = ''

        self.content = ''
        self.article_url = ''

        self.original_pictures = []
        self.retweet_pictures = None
        self.original = None
        self.video_url = ''

        self.publish_place = ''
        self.publish_time = ''
        self.publish_tool = ''

        self.up_num = 0
        self.retweet_num = 0
        self.comment_num = 0

    def __str__(self):
        """打印一条微博"""
        result = self.content + '\n'
        result += u'微博发布位置：%s\n' % self.publish_place
        result += u'发布时间：%s\n' % self.publish_time
        result += u'发布工具：%s\n' % self.publish_tool
        result += u'点赞数：%d\n' % self.up_num
        result += u'转发数：%d\n' % self.retweet_num
        result += u'评论数：%d\n' % self.comment_num
        result += u'url：https://weibo.cn/comment/%s\n' % self.id
        return result


# 微博的关键信息信息
class WeiboKey:
    def __init__(self):
        self.uid = 123456  # 用户 ID，对应 user.id
        self.wid = ''  # 微博唯一ID，对应 mblogid
        self.mid = 123456  # 微博评论ID, 形如 4759260203849298

    def __str__(self):
        """打印一条微博"""
        result = "uid: %s, wid: %s, mid: %s" % (self.uid, self.wid, self.mid)
        return result

class User():
    # 用户信息
    def __int__(self):
        self.user_id = 2656274875   # 用户 ID，形如 2656274875
        self.user_screen_name = 'ha'  # 微博用户名, 形如 央视新闻
        self.user_domain = 'cctv'  # 微博用户域名，形如 cctvxinwen

class WeiboInfo(User):
    def __int__(self):
        self.created_at = 'Sun Apr 17 15:10:22 +0800 2022'
        self.attitudes_count = 0  # 点赞数量
        self.comments_count = 0  # 所有评论数量
        self.reads_count = 0  # 阅读数量
        self.reposts_count = 0  # 转发数量
        self.text_raw = 'haha'  # 评论原文
        self.source = 'web'  # 发布来源

    def Title(self):
        return u"用户名, 用户ID, 用户域名, 发布来源, 微博正文"

    def __str__(self):
        result = "user_name"
        self.user_screen_name


class CommentInfo(User):
    def __int__(self):
        self.created_at = 'Sun Apr 17 15:10:22 +0800 2022'
        self.floor_num = 0  # 楼层数量
        self.mid = 0  # 评论 ID，形如 4759260203849298
        self.text_raw = ''  # 评论内容
