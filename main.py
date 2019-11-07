import random
import time
import os
from pprint import pprint
import json
import requests
from pyppeteer import launch
import asyncio
import smtplib
from email.mime.image import MIMEImage
from email.header import Header
import schedule

with open('UA.in') as f:
    ua_list = [x.split('\n')[0] for x in f.readlines()]

get_random_ua = lambda: random.choice(ua_list)
SECRET_PASS = 'your secret pass'
reply_message = '📢 在最美的年华，做最喜欢的事情的说，别辜负了美好时光。借时光之手，暖一处花开，借一方晴空，拥抱梦想的说。早安的说！'

no_cat = True


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
                    # await weibo-qq-login and reply
                    asyncio.get_event_loop().run_until_complete(reply())
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
    await page.goto(url='https://passport.weibo.cn/signin/other?r=https%3A%2F%2Fm.weibo.cn')
    url = page.url
    print(url)
    await page.click('i[class="icon forQQ"]')
    # 等待二维码
    await asyncio.sleep(5)
    await page.screenshot({'path': './weibo-qq-login.png', 'quality': 100, 'fullPage': True})
    # 发送邮件
    mail_smtp()
    # os.remove('./weibo-qq-login.png')
    await asyncio.sleep(10)
    cookies=await page.cookies()
    print(cookies)
    return page.cookies
    await page.goto(cat_scheme)
    while True:
        try:
            await page.type(
                selector='#app > div.lite-page-wrap > div > div.lite-page-editor > div > div > div > div.textarea-box > textarea:nth-child(1)',
                text=reply_message
            )
            await page.click(
                '#app > div.lite-page-wrap > div > div.lite-page-editor > div > div > div > div.flex-row.composer-mini-bar > button')
            await asyncio.sleep(5)
        except:
            await asyncio.sleep(1)
        else:
            break



def mail_smtp():
    mail_host = 'smtp.qq.com'
    mail_pass = SECRET_PASS

    mail_user = '616200285@qq.com'
    to_list = ['wohfacm@163.com']
    with open('./weibo-qq-login.png', 'rb') as png:
        message = MIMEImage(png.read())
    message['From'] = mail_user
    message['To'] = ",".join(to_list)

    subject = 'A岛登陆啦'  # 邮件主题
    message['Subject'] = Header(subject, 'utf-8')
    message.add_header('Content-Disposition', 'attachment', filename="weibo-qq-login.png")
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, to_list, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e.args)
        print("Error: 无法发送邮件")


def test():
    crawler()


def main():
    schedule.every(5).minutes.at(':05').do(crawler)
    schedule.every(5).minutes.at(':06').do(crawler)
    schedule.every(5).minutes.at(':07').do(crawler)
    schedule.every(5).minutes.at(':08').do(crawler)
    schedule.every(5).minutes.at(':09').do(crawler)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    test()
