import logging
import re
import sys
from datetime import datetime, timedelta

from .. import datetime_util
from ..weibo import Weibo
from .comment_parser import CommentParser
from .mblog_picAll_parser import MblogPicAllParser
from .parser import Parser
from .util import handle_garbled, handle_html, to_video_download_url

logger = logging.getLogger('spider.wb_comment_parser')


class WbCommentParser(Parser):
    # 爬取微博内容及评论内容
    def __init__(self, cookie, topic):
        self.cookie = cookie
        self.topic = topic
        self.url = "https://s.weibo.com/weibo?q=%23%s%23" % (topic)
        self.selector = handle_html(self.cookie, self.url)

    def get_weibo_content(self):
        # 获取微博内容
        try:
            pass
        except Exception as e:
            logger.exception(e)

    def get_comment(self):
        # 获取微博评论
        pass
