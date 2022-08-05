import copy
import logging
import sys

from .writer import Writer

logger = logging.getLogger('spider.mongo_writer')


class MongoWriter(Writer):
    def __init__(self):
        pass

    def _info_to_mongodb(self, collection, info_list):
        """将爬取的信息写入MongoDB数据库"""
        try:
            import pymongo
        except ImportError:
            logger.warning(
                u'系统中可能没有安装pymongo库，请先运行 pip install pymongo ，再运行程序')
            sys.exit()
        try:
            from pymongo import MongoClient

            client = MongoClient()
            db = client['weibo']
            collection = db[collection]
            new_info_list = copy.deepcopy(info_list)
            for info in new_info_list:
                if not collection.find_one({'id': info['id']}):
                    collection.insert_one(info)
                else:
                    collection.update_one({'id': info['id']}, {'$set': info})
        except pymongo.errors.ServerSelectionTimeoutError:
            logger.warning(
                u'系统中可能没有安装或启动MongoDB数据库，请先根据系统环境安装或启动MongoDB，再运行程序')
            sys.exit()

    def write_weibo(self, weibos):
        """将爬取的微博信息写入MongoDB数据库"""
        weibo_list = []
        for w in weibos:
            w.user_id = self.user.id
            weibo_list.append(w.__dict__)
        self._info_to_mongodb('weibo', weibo_list)
        logger.info(u'%d条微博写入MongoDB数据库完毕', len(weibos))

    def write_user(self, user):
        """将爬取的用户信息写入MongoDB数据库"""
        self.user = user
        user_list = [user.__dict__]
        self._info_to_mongodb('user', user_list)
        logger.info(u'%s信息写入MongoDB数据库完毕', user.nickname)

    def write_topic_wb_comments(self, topic, wb, comment_list):
        """将爬取的信息写入MongoDB数据库，已存在的微博不插入、已存在的评论不插入"""
        try:
            import pymongo
        except ImportError:
            logger.warning(
                u'系统中可能没有安装pymongo库，请先运行 pip install pymongo ，再运行程序')
            sys.exit()
        try:
            from pymongo import MongoClient

            client = MongoClient()
            db = client['wbc']  # 数据库名称 wbc, weibo comment
            topic_collection = db[topic]  # 每个词条分为一个集合

            exist_wb = topic_collection.find_one({'id': wb['id']})
            if not exist_wb:
                topic_collection.insert_one(wb)
            else:
                # 可能需要更新微博
                print('Need to update weibo')

            # 更新微博评论
            comment_array_key = 'comments'
            for comment in comment_list:
                if not topic_collection.find_one({'id': wb['id'], comment_array_key: {'$exists': True}}):
                    # comments 操作组不存在，插入一个
                    topic_collection.update_one({'id': wb['id']}, {'$set': {comment_array_key: [comment]}})
                elif not topic_collection.find_one({'id': wb['id'], comment_array_key + '.id': comment['id']}):
                    # 当前评论尚不存在，插入它
                    topic_collection.update_one({'id': wb['id']}, {'$push': {comment_array_key: comment}})
                else:
                    # 评论已存在，不需要操作
                    pass

        except pymongo.errors.ServerSelectionTimeoutError:
            logger.warning(
                u'系统中可能没有安装或启动MongoDB数据库，请先根据系统环境安装或启动MongoDB，再运行程序')
            sys.exit()
        except Exception:
            logger.warning("遇到了失败")
