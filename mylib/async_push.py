import asyncio
from tools.push_tools import PushTool
from aiohttp import ClientSession, TCPConnector
from datetime import datetime

# 数据库配置
success_num = 0
fail_num = 0


async def register_user(session, cookie_jar):
    global success_num
    global fail_num
    global start_time
    referer = PushTool.get_url('http://www.61k.com/lsj')
    r = PushTool.get_url('http://www.61k.com/lsj')
    headers = {
        'User-Agent': PushTool.user_agent(),
        'Referer': referer,
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'api.share.baidu.com',
    }
    status = 233
    try:
        payload = {
            'r': r,
            'l': referer,
        }
        async with ClientSession(cookies=cookie_jar) as session:
            async with session.post(url='http://api.share.baidu.com/s.gif', data=payload, headers=headers, timeout=2) as response:
                r = await response.read()
                if r == b'' and response.status == 200:
                    success_num += 1
                else:
                    fail_num += 1
                status = response.status
    except Exception as e:
        fail_num += 1
    this_time = datetime.now()
    spend = this_time - start_time
    speed_sec = int(success_num / spend.seconds)
    speed_day = (speed_sec * 60 * 60 * 24)/10000000
    percent = success_num / (fail_num + success_num) * 100
    print("%s 成功%s 预计(day/千万):%s M 成功率:%.2f%% 状态码:%s" % (datetime.now(), success_num, speed_day, percent, status))


async def bound_register(sem, session, cookie_jia):
    # 使用Semaphore， 它会在第一批2000个请求发出且返回结果(是否等待返回结果取决于你的register_user方法的定义)后
    # 检查本地TCP连接池(最大2000个)的空闲数(连接池某个插槽是否空闲，在这里，取决于请求是否返回)
    # 有空闲插槽，就PUT入一个请求并发出(完全不同于Jmeter的rame up in period的线性发起机制).
    # 所以，在结果log里，你会看到第一批请求(开始时间)是同一秒发起，而后面的则完全取决于服务器的吞吐量
    async with sem:
        await register_user(session, cookie_jia)


async def run(num):
    tasks = []
    # Semaphore， 相当于基于服务器的处理速度和测试客户端的硬件条件，一批批的发
    # 直至发送完全部（下面定义的number/num）
    sem = asyncio.Semaphore(2000)
    # 创建session，且对本地的TCP连接不做限制limit=0
    # 超时时间指定
    # total:全部请求最终完成时间
    # connect: aiohttp从本机连接池里取出一个将要进行的请求的时间
    # sock_connect：单个请求连接到服务器的时间
    # sock_read：单个请求从服务器返回的时间
    import aiohttp
    # timeout = aiohttp.ClientTimeout(total=300, connect=60, sock_connect=60, sock_read=60)
    async with ClientSession(connector=TCPConnector(limit=0)) as session:
        while True:
            cookie_jar = PushTool.get_cookies()
            for i in range(0, num):
                # 如果是分批的发，就使用并传递Semaphore
                task = asyncio.ensure_future(bound_register(sem=sem, session=session, cookie_jia=cookie_jar))
                tasks.append(task)
            responses = asyncio.gather(*tasks)
            await responses


start_time = datetime.now()
loop = asyncio.get_event_loop()
num = 1000
future = asyncio.ensure_future(run(num))
loop.run_until_complete(future)
loop.run_until_complete(asyncio.sleep(0))
loop.close()

