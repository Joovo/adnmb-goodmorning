import random
import time
import os
from pprint import pprint
import json
import requests
from pyppeteer import launch
import asyncio
import schedule

with open('UA.in') as f:
    ua_list = [x.split('\n')[0] for x in f.readlines()]

get_random_ua = lambda: random.choice(ua_list)
SECRET_PASS = 'your secret pass'
phone = 'your phone num'
password = 'your pwd'

no_cat = True
reply_message = '📢 在最美的年华，做最喜欢的事情的说，别辜负了美好时光。借时光之手，暖一处花开，借一方晴空，拥抱梦想的说。早安的说！'

def run_for_no_cat(fun):
    def empty_f():
        pass

    return fun if no_cat else empty_f


@run_for_no_cat
def crawler():
    header = {
        'User-Agent': get_random_ua()
    }
    response = requests.get(
        'https://m.weibo.cn/api/container/getIndex?type=uid&value=5648729445&containerid=1076035648729445',
        headers=header)
    try:
        data = json.loads(response.text)
        pprint(data)
    except TypeError as e:
        print(e.args)
    finally:
        if data.get('ok'):
            cards = data.get('data', {}).get('cards', {})
            try:
                text = cards[1]['mblog']['text']
                if text.startswith('咕猫') or True:
                    no_cat = False
                    cat_scheme = cards[1]['scheme']
                    # await login and reply
                    asyncio.get_event_loop().run_until_complete(reply(cat_scheme))
            except IndexError as ie:
                print(ie.args)


async def reply(cat_scheme: str = ''):
    # create_url = 'https://m.weibo.cn/api/comments/create'
    browser = await launch(
        headless=False,
        # ignoreDefaultArgs="--enable-automation"
    )
    page = await browser.newPage()
    await page.setUserAgent(get_random_ua())
    await page.setJavaScriptEnabled(enabled=True)
    await page.goto(
        url='https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn')
    await asyncio.sleep(5)
    await page.type(selector='input#loginName', text=phone)
    await page.type(selector='input#loginPassword', text=password)

    await page.click('a#loginAction')
    await asyncio.sleep(5)
    await page.goto(cat_scheme)
    await asyncio.sleep(5)
    await page.click('span[class="m-box-center-a main-text m-text-cut focus"]')
    await asyncio.sleep(2)
    await page.type(selector='textarea[placeholder="发表评论"]', text=reply_message)
    await page.click('button[class="btn-send"]')
    await asyncio.sleep(10)

def test():
    crawler()


def init_cat():
    global no_cat
    no_cat = True


def main():
    schedule.every().day.at(':00').do(init_cat())

    schedule.every(5).minutes.at(':05').do(crawler)
    schedule.every(5).minutes.at(':06').do(crawler)
    schedule.every(5).minutes.at(':07').do(crawler)
    schedule.every(5).minutes.at(':08').do(crawler)
    schedule.every(5).minutes.at(':09').do(crawler)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
