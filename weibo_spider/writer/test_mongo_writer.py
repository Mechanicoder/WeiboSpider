import pymongo


def test():
    client = pymongo.MongoClient()
    db = client['blog_db']
    # collections = client['wbc']['weibo_comments']

    collection_name = 'blog_collection'
    # doc = collections[topic]
    blog_json = {
        'id': 1234567890,
        'date': '2022年5月2日',
        'time': '16点42分',
        'location': '江苏省',
        'TabsInBrowser': {
            'first': 'bing',
            'second': 'csdn',
            'third': 'baidu',
            'fourth': 'eo',
            'number': 4
        },
        'mood': 'happy'
    }

    # 检查是否存在，如存在则更新、否则替换
    find_id = {
        'id': blog_json['id']
    }
    collection = db[collection_name]
    result = collection.find_one(filter=find_id)
    if not result:
        collection.insert_one(blog_json)
    else:
        print('The id of test_json already exits, nothing changed.')

    # 初始数组
    update_data = [
        {'id': 10, 'prime': [1, 3, 5, 7, 11, 13, 17]},
        {'id': 11, 'even': [2, 4, 6, 8, 10, 12, 14]},
    ]

    # 更新数组
    collection.update_one({'id': 1234567890}, {'$set': {'numbers': update_data}})

    # 新的数组
    update_data = [
        {'id': 10, 'prime': [1, 3, 5, 7, 11, 13, 17]},
        {'id': 11, 'even': [2, 4, 6, 8, 10, 12, 14]},
        {'id': 12, 'odd': [1, 3, 5, 7, 9, 11, 13]}
    ]
    for num in update_data:
        if not collection.find_one({'id': 1234567890, 'numbers.id': num['id']}):
            # 为数组添加元素，使用 push
            collection.update_one({'id': 1234567890}, {'$push': {'numbers': num}})
        else:
            # 已存在，不需要操作
            pass
    if collection.find_one({'id': 1234567890, 'numbers': {'$exists': True}}):
        print('numbers exists')
    return
    # result = client['wbc']['weibo_comments'].update_one({"item": "journal"},{"$set": {"size.uom": "nmn", "status": "XXXXXXXXXXX"}, "$currentDate": {"lastModified": True}},)

    docs = collections.find()
    print('All documents of object info: ', docs)

    print('Every document in docs is:')
    for x in docs:
        print(x)

    # 获取的是完整一个文档
    print('Method of <find_one> is ')
    doc = collections.find_one({'topic': {'$exists': True}})
    print(doc)

    # comments = doc['topic'][0]['comments']
    # print(comments)

    print('test finished')


test()
