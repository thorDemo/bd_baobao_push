from threadpool import ThreadPool, makeRequests
from configparser import ConfigParser
import os
import time
from mylib.https_push import https_push

config = ConfigParser()
config.read('push_config.ini', 'utf-8')
thread_num = int(config.get('bd_push', 'thread'))
target = config.get('bd_push', 'target')

size = 0
line_cache = 0
while True:
    f_size = os.path.getsize(target)
    if f_size != size:
        print('什么？新的风暴已经出现！')
        lines = open(target, 'r', encoding='UTF-8')
        temp = 0
        arg = []
        pool = ThreadPool(thread_num)
        for line in lines:
            if line_cache <= temp:
                print(line)
                arg.append(line)
            temp += 1
        request = makeRequests(https_push, arg)
        [pool.putRequest(req) for req in request]
        pool.wait()
        line_cache = temp
        lines.close()
    size = f_size
    time.sleep(1)

# if https == 1:
#     from mylib.https_push import https_push
#     pool = ThreadPool(thread_num)
#     arg = []
#     for x in range(0, thread_num):
#         arg.append(target)
#     request = makeRequests(https_push, arg)
#     [pool.putRequest(req) for req in request]
#     pool.wait()
# elif https == 0:
#     from mylib.push_without_proxy import push_url_two
#     pool = ThreadPool(thread_num)
#     arg = []
#     for x in range(0, thread_num):
#         arg.append(target)
#     request = makeRequests(push_url_two, arg)
#     [pool.putRequest(req) for req in request]
#     pool.wait()
