import requests
import matplotlib.pyplot
import numpy
from bs4 import BeautifulSoup
import re
import json
import datetime
import argparse

'''tmp = ' '

def get_data_today():
    current_date = datetime.datetime.now()
    print(current_date.year)
    tmp1 = f'{current_date.day:02}'
    tmp2 = f'{current_date.month:02}'
    tmp3 = f'{current_date.year}'
    tmp = tmp1 + '.' + tmp2 + '.' + tmp3
    print(tmp)

get_data_today()'''

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", help="enter string to search", default="4851004/10001")
parser.add_argument("-d", "--date", help="enter date (DD.MM.YYYY)", default="03.04.2023")
parser.add_argument("--graph", help="enter key to hide graph", action="store_true")
args = parser.parse_args()

table = [0, 0, 0, 0, 0, 0, 0]

def get_json(response):
    start_json = re.search(r"window\.__INITIAL_STATE__ = (.*?);", response).group(1)
    json_with_groups = json.loads(start_json)
    return json_with_groups


def find_group(name):
    number_of_groups_found = 0
    find_group_url = 'https://ruz.spbstu.ru/search/groups?q=' + name.replace(' ', '%20')
    response = requests.get(find_group_url).text
    json_with_groups = get_json(response)
    found_groups = []
    if "searchGroup" in json_with_groups:
        raw_found_groups = json_with_groups["searchGroup"]["data"]
        number_of_groups_found = len(raw_found_groups)
        for group in range(number_of_groups_found):
            group_name = raw_found_groups[group]["name"]
            group_id = raw_found_groups[group]["id"]
            group_faculty = raw_found_groups[group]["faculty"]["id"]
            found_groups.append({"name": group_name, "group_id": group_id, "faculty": group_faculty})
    if number_of_groups_found:
        number_group = 0
        print('Найдены группы:')
        for group in range(number_of_groups_found):
            print(str(group + 1) + ' - ' + found_groups[group]["name"])
        if number_of_groups_found != 1:
            print("Выберите группу (1 - " + str(number_of_groups_found) + "): ", end='')
            number_group = int(input()) - 1
            if number_group < 0 or number_group > number_of_groups_found - 1:
               print('Некорректное значение группы')
               return {}
    else:
        print('Группы не найдены')
        return {}
    print()
    return found_groups[number_group]

def get_daily_table(study_week, input_date):
    number_of_pairs = 0
    output = ""
    for i in range(len(study_week)):
        date = datetime.datetime.strptime(study_week[i]["date"], "%Y-%m-%d").strftime("%d.%m.%Y")
        if date == input_date:
            number_of_pairs += 1
            if study_week[i]["weekday"] == 1:
                week_day = 'Понедельник'
            elif study_week[i]["weekday"] == 2:
                week_day = 'Вторник'
            elif study_week[i]["weekday"] == 3:
                week_day = 'Среда'
            elif study_week[i]["weekday"] == 4:
                week_day = 'Четверг'
            elif study_week[i]["weekday"] == 5:
                week_day = 'Пятница'
            elif study_week[i]["weekday"] == 6:
                week_day = 'Суббота'
            elif study_week[i]["weekday"] == 7:
                week_day = 'Воскресенье'
            lessons = study_week[i]["lessons"]
            output += week_day + ' (' + date + ')\n'
            for j in range(len(lessons)):
                audience = ''
                teacher = ''
                subject_name = lessons[j]["subject"] + '\n   '
                type_subject = lessons[j]["typeObj"]["name"] + '\n   '
                time_start = lessons[j]["time_start"] + '-'
                time_end = lessons[j]["time_end"] + '\n   '
                if "teachers" in lessons[j] and lessons[j]["teachers"]:
                    teacher = lessons[j]["teachers"][0]["full_name"] + '\n   '
                if "auditories" in lessons[j] and lessons[j]["auditories"]:
                    audience = lessons[j]["auditories"][0]["building"]["name"]
                    audience += ', ауд. ' + lessons[j]["auditories"][0]["name"] + '\n'

                output += str(j + 1) + '. ' + time_start + time_end + subject_name + type_subject + teacher + audience
            output += '\n'
    if not number_of_pairs:
        output += 'Вам не нужно идти на пары, если их нет'
    return output


def get_title(response, date):
    soup = BeautifulSoup(response, "lxml")
    item = soup.find("div", {'id': 'rootPageContainer', 'class': 'page__container'})
    title = item.find("h3").text + '\n'
    title = re.search(r'\(.*?\)', title).group()
    title = 'Расписание на неделю с днём ' + date + ' ' + title + '\n'
    return title

def get_table(group, date):
    group_name = str(group['name'])
    group_id = str(group['group_id'])
    group_faculty = str(group['faculty'])

    get_table_url = 'https://ruz.spbstu.ru/faculty/' + group_faculty + '/groups/' + group_id + '?date='
    get_table_url += datetime.datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
    response = requests.get(get_table_url).text
    json_with_table = get_json(response)
    title = get_title(response, date)

    output = 'Группа: ' + group_name + '\n' + title + '\n'
    study_week = json_with_table['lessons']['data'][group_id]
    output += get_daily_table(study_week, date)
    for i in range(len(study_week)):
        table[study_week[i]["weekday"] - 1] = len(study_week[i]["lessons"])
    return output

def print_graph(graph, output):
    title = re.search(r"Расписание.*неделя\)", output).group(0)
    x_list = list(range(0, 7))
    x_indexes = numpy.arange(len(x_list))
    matplotlib.pyplot.setp('r')
    matplotlib.pyplot.figure(figsize=(9, 5))
    matplotlib.pyplot.title(title)
    matplotlib.pyplot.xlabel('День недели')
    matplotlib.pyplot.ylabel('Количество пар')
    matplotlib.pyplot.bar(x_indexes, table)
    week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    matplotlib.pyplot.xticks(x_indexes, week_days)
    if not graph:
        matplotlib.pyplot.show()

if __name__ == '__main__':
    found_group = find_group(args.search)
    if found_group:
        output = get_table(found_group, args.date)
        print(output)
        print_graph(args.graph, output)

    parser.print_help()
