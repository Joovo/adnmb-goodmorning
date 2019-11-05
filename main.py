import random
import requests
from requests import sessions
from pprint import pprint
import json
from pyppeteer import launch
import asyncio

with open('UA.in') as f:
    ua_list = [x for x in f.readlines()]

get_random_ua = lambda: str(random.choice(ua_list)).split('\n')[0]

message = '📢 在最美的年华，做最喜欢的事情的说，别辜负了美好时光。借时光之手，暖一处花开，借一方晴空，拥抱梦想的说。早安的说！'


def crawler(sess):
    header = {
        'User-Agent': get_random_ua()
    }
    response = sess.get(
        'https://m.weibo.cn/api/container/getIndex?type=uid&value=5648729445&containerid=1076035648729445',
        headers=header)
    try:
        data = json.loads(response.text)
    except TypeError as e:
        print(e.message)
    finally:
        pprint(data)
        if data.get('ok'):
            cards = data.get('cards')
            try:
                text = cards[1]['text']
                if text.startswith('咕猫'):
                    cat_scheme = cards[1]['scheme']
                    return cat_scheme
            except IndexError as ie:
                print(ie.message)


async def reply(cat_scheme: str = ''):
    # create_url = 'https://m.weibo.cn/api/comments/create'
    browser = await launch(
        headless=False,
        # ignoreDefaultArgs="--enable-automation"
    )
    page = await browser.newPage()
    await page.setUserAgent(get_random_ua())
    await page.setJavaScriptEnabled(enabled=True)
    await page.goto(url='https://passport.weibo.cn/signin/other?r=https%3A%2F%2Fm.weibo.cn')
    # href = await page.xpath('//*[@id="app"]//a[@class="b-left"]')
    # login_href=await href[0].jsonValue()
    # print(login_href)
    url=page.url
    print(url)
    # await page.click('a[class=link]')
    # await page.type(selector='input#u', text='123')
    # await page.type(selector='input#p',text='123')
    # await page.click('a[class=link]')
    await asyncio.sleep(1)

    # await page.click('p[class=label]/a')
    # await page.goto(cat_scheme)
    # await page.type('')
    # await page
    # await page.close()
    await asyncio.sleep(1000)


def test():
    asyncio.get_event_loop().run_until_complete(reply())


if __name__ == "__main__":
    # sess = sessions.Session()
    # cat_scheme = crawler(sess)
    # reply(cat_scheme)
    # asyncio.get_event_loop().run_until_complete(reply())
    # sess.close()
    test()
