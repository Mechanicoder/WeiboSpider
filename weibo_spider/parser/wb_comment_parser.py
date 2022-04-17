import logging
import re
import sys
from datetime import datetime, timedelta
import json

from .. import datetime_util
from ..weibo import Weibo, User, WeiboInfo, CommentInfo
from .comment_parser import CommentParser
from .mblog_picAll_parser import MblogPicAllParser
from .parser import Parser
from .util import handle_garbled, handle_html, to_video_download_url

logger = logging.getLogger('spider.wb_comment_parser')


def ParserUser(user_json):
    # 解析用户信息
    if user_json:
        user = User()
        user.user_id = user_json['id']
        user.user_screen_name = user_json['screen_name']
        user.user_domain = user_json['domain']
        return user
    else:
        return User()


class WbCommentParser(Parser):
    # 爬取微博内容及评论内容
    def __init__(self, cookie, wb_key):
        self.cookie = cookie
        self.weibo_key = wb_key

        self.all_comments = []

    def make_weibo_url(self):
        # 获取微博 json 数据的 url
        return 'https://weibo.com/ajax/statuses/show?id=%s' % self.weibo_key.wid

    def make_comment_url(self, max_id, count):
        # 获取微博评论 json 数据的 url， show_bulletin=0,1,2 分别
        # 经测试，count 最大支持200，且当数量超过100时，反馈结果会被分为两个组 [0, 99], [100, 199]
        if max_id > 0:
            # 数据访问接口：从 max_id 开始，找到总数量为 count 的评论
            return 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=%d&is_show_bulletin=2&max_id=%d&count=%d' % (
                self.weibo_key.mid, max_id, count)
        else:
            return 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=%d&is_show_bulletin=2&count=%d' % (
                self.weibo_key.mid, count)

    def get_weibo_content(self):
        # 获取微博内容
        try:
            wb_url = self.make_weibo_url()
            wb_json = handle_html(self.cookie, wb_url, 'json')
            if wb_json:
                check_mid = int(wb_json['mid'])
                if check_mid == self.weibo_key.mid:
                    # 开始解析微博
                    wb = WeiboInfo()
                    wb = ParserUser(wb_json['user'])
                    wb.created_at = wb_json['created_at']
                    wb.attitudes_count = wb_json['attitudes_count']
                    wb.comments_count = wb_json['comments_count']
                    wb.reads_count = wb_json['reads_count']
                    wb.reposts_count = wb_json['reposts_count']
                    wb.text_raw = wb_json['text_raw']
                    wb.source = wb_json['source']
                    return wb
                else:
                    print(u'用户 %s 的微博 %s 爬取失败' % (self.weibo_key.uid, self.weibo_key.wid))
        except Exception as e:
            logger.exception(e)

    def parse_comment(self, comment_json):
        if comment_json:
            comment = CommentInfo()
            comment = ParserUser(comment_json['user'])
            comment.created_at = comment_json['created_at']
            comment.floor_num = comment_json['floor_number']
            comment.mid = comment_json['id']  # id 是数字
            comment.text_raw = comment_json['text_raw']
            return comment
        else:
            return CommentInfo()

    def get_one_page_comment(self, comment_page_url):
        comments_json = handle_html(self.cookie, comment_page_url, 'json')
        if comments_json:
            max_id = comments_json['max_id']  # 更新 max_id
            for idx in range(0, len(comments_json['data'])):
                one_comment = comments_json['data'][idx]
                self.all_comments.append(self.parse_comment(one_comment))
            return max_id
        else:
            return -1

    def get_comments(self):
        # 获取微博评论
        try:
            # 初始时不需要 max_id
            # max_id 可能是每条评论的唯一 ID，在整个 weibo.com 下具有唯一性
            max_id = -1
            count = 20  # 和浏览器数值保持相同：经测试，最大值支持到 200
            cnt_step = 20
            comment_url = self.make_comment_url(max_id, count)
            max_id = self.get_one_page_comment(comment_url)
            while -1 != max_id:
                comment_url = self.make_comment_url(max_id, count)
                max_id = self.get_one_page_comment(comment_url)
                print(u'已获得评论数量 ', len(self.all_comments), ' max_id ', max_id)

            print(u'获得总评论数量 ', len(self.all_comments))
            return self.all_comments
        except Exception as e:
            logger.exception(e)
