import logging
import re
import sys
from datetime import datetime, timedelta
import json

from .. import datetime_util
from ..weibo import Weibo
from .comment_parser import CommentParser
from .mblog_picAll_parser import MblogPicAllParser
from .parser import Parser
from .util import handle_garbled, handle_html, to_video_download_url

logger = logging.getLogger('spider.wb_comment_parser')


class WbCommentParser(Parser):
    # 爬取微博内容及评论内容
    def __init__(self, cookie, wb_key):
        self.cookie = cookie
        self.weibo_key = wb_key

    def make_weibo_url(self):
        # 获取微博 json 数据的 url
        return 'https://weibo.com/ajax/statuses/show?id=%s' % self.weibo_key.wid

    def make_comment_url(self, max_count):
        # 获取微博评论 json 数据的 url
        return 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=%&is_show_bulletin=2&count=%' % (self.weibo_key.mid, max_count)

    def get_weibo_content(self):
        # 获取微博内容
        try:
            wb_url = self.make_weibo_url()
            wb_json = handle_html(self.cookie, wb_url, 'json')
            if wb_json:
                test_mid = int(wb_json['mid'])
                if test_mid == self.weibo_key.mid:
                    print('测试成功')
                else:
                    print('测试失败')
        except Exception as e:
            logger.exception(e)

    def get_comment(self):
        # 获取微博评论
        pass
