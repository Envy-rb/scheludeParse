import json
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime


def parse_pair(pair):
	result = {}
	if pair.select('div.left-column'):
		left = pair.select('div.left-column')[-1]
		right = pair.select('div.right-column')[-1]
		subject = ((left.select('.subject')[0]).select('a')[0].text)
		teacher = ((left.select('.teacher')[0]).select('a')[0].text)
		classroom = ((right.select('.place')[0]).select('a')[0].text)

		if subject.strip():
			result['subject'] = subject
		if teacher.strip():
			result['teacher'] = teacher
		if classroom.strip():
			result['classroom'] = classroom
	else:
		result['subject'] = 'Нет пары'

	return result


def parse_pairs(offset = 0):
	url = 'https://kbp.by/rasp/timetable/view_beta_kbp/?cat=group&id=41'
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	r = requests.get(url, headers = headers)
	html = BS(r.content, 'html.parser')
	table =  html.find('table')
	result = []
	currentDay = datetime.today().weekday()
	trIndex = 1
	trIndex += currentDay
	trIndex += offset
	if (trIndex > 7):
		trIndex = 0 + offset
	for x in range(1,8):
		pairs = table.find_all('tr')[x + 1]
		pair = pairs.find_all('td')[trIndex]
		result.append(parse_pair(pair))
		pass
	return result


def parse_groups():
	groups = {}
	url = 'https://kbp.by/rasp/timetable/view_beta_kbp/?cat=group&id='
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	for x in range(0, 100):
		activeUrl = url + str(x)
		r = requests.get(activeUrl, headers=headers)
		html = BS(r.content, 'html.parser')
		header = html.find(id = 'right_block')
		group = header.find(class_='style_text')
		groupNum = group.text.strip()[-5:]
		if ('-' in groupNum):
			groups[groupNum] = x
	with open('datares/schelude/groups.json', 'w') as groupsJson:
		json.dump(groups, groupsJson, indent=4)

def get_groups():
	with open('datares/schelude/groups.json') as groupsJson:
		return(json.load(groupsJson))

for pair in parse_pairs(1):
	print(pair)