
from time import sleep
from requests import get,post
import urllib3
urllib3.disable_warnings()
try:
    with open('lastitem', 'r+') as f:
        articles = f.read()
except FileNotFoundError:
    with open('lastitem', 'w+') as f:
        f.write('0')
        articles = '0'
print('Last sent item:', articles)
headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Connection": "keep-alive", "Referer": "https://codal360.ir/fa/", "User-Agent": "Mozilla/5.0 (Windows NT 6.3; rv:68.0) Gecko/20100101 Firefox/68.0", "X-Requested-With": "XMLHttpRequest"}
data = get(url='https://codal360.ir/fa/search_statement_result/?s_type=100&number_row=20&page=1', headers = headers, verify=False)
data = data.json()
for article in data['result'][::-1]:
    id = str(article['id'])
    s = article['symbol']
    title = article['title']
    html_link = article['html_link']
    date = article['publish_date']
    if int(id) > int(articles):
        t = "#" + s + "\n\n<a href='" + html_link + "'>" + title + "</a>\n"
        if article['attachment_link'] is not None: t = t + '<a href ="' + article['attachment_link'] + '">ضـمائـم</a>'
        t = t + '\nمنتشر شده در تاريخ: ' + date
        tg = post(url='https://api.telegram.org/bot{token}/sendMessage?chat_id=@asarmaye&parse_mode=HTML', verify=False, data={"text": t})
        sleep(4)
    else:
        print(id, 'exists!')
print('Last item:', id)
with open('lastitem', 'w+') as f:
    f.write(id)


