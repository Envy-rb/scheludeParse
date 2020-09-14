import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime

def parsePair(pair):
    result = ""
    if pair.select('div.left-column'):
        left = pair.select('div.left-column')[0]
        right = pair.select('div.right-column')[0]
        subject = ((left.select('.subject')[0]).select('a')[0].text)
        teacher = ((left.select('.teacher')[0]).select('a')[0].text)
        classroom = ((right.select('.place')[0]).select('a')[0].text)

        result += subject + '\n'
        result += teacher + '\n'
        result += classroom + '\n'
    else:
        result += 'Нет пары'

    return result

def parsePairs(offset = 0):
    url = 'https://kbp.by/rasp/timetable/view_beta_kbp/?cat=group&id=41'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers = headers)
    html = BS(r.content, 'html.parser')
    table =  html.find('table')
    result = ""
    currentDay = datetime.today().weekday()
    trIndex = 1
    trIndex += currentDay
    trIndex += offset

    for x in range(1,8):
        pairs = table.find_all('tr')[x + 1]
        pair = pairs.find_all('td')[trIndex]
        result += str(x) + '.'
        result += parsePair(pair)
        result += '\n'
        pass
    return result