from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import sys
import json
from matplotlib import pyplot as plt


def formating_date(date: str, sep: str, sep_out: str) -> str:
    date_arr = date.split(sep)
    date_arr.reverse()
    date = ''
    for i in date_arr:
        date = date + i + sep_out
    return date[:-1]


def draw_graph(week) -> None:
    dates = []
    lessons = []
    count_days = 1
    for day in week:
        if (count_days != day['weekday']):  # to show day with null lessons
            dt = datetime.strptime(prev_date, '%Y-%m-%d')
            result = dt + timedelta(days=1)
            day_reverse = formating_date(
                datetime.strftime(result, '%Y-%m-%d')[5:], '-', '.')
            dates.append(day_reverse)
            lessons.append(0)
            prev_date = datetime.strftime(result, '%Y-%m-%d')[0:10]
            count_days += 1

        day_reverse = formating_date(day['date'][5:], '-', '.')
        dates.append(day_reverse)
        lessons.append(len(day['lessons']))
        prev_date = day['date']
        count_days += 1

    plt.bar(dates, lessons, color='maroon', width=0.5)
    plt.xlabel("Days of week")
    plt.ylabel("Count of lessons")
    plt.title("Graph")
    plt.show()


def script_parse(url: str) -> dict:
    try:
        res = requests.get(url)
    except ConnectionError:
        print('Connection error')
        return None
    soup = BeautifulSoup(res.text, "html.parser")
    for find in soup.find_all('script'):
        if 'window.__INITIAL_STATE__' in find.get_text():
            found = find.get_text()[33:-3]
    return json.loads(found)


def main():

    format_date = formating_date(sys.argv[1], '.', '-')

    url = 'https://ruz.spbstu.ru/faculty/122/groups/'

    dictionary = script_parse(url)
    if dictionary == -1:
        return

    for index in dictionary['groups']['data']['122']:
        if index['name'] == sys.argv[2]:
            id_group = index['id']
            break

    url = url + str(id_group) + '?date=' + format_date

    dictionary = script_parse(url)

    print('\nЧётная неделя' + '\n') if dictionary['lessons']['week']['is_odd']\
        else print('\nНечётная неделя' + '\n')

    for all_lessons in dictionary['lessons']['data'][str(id_group)]:
        format_date = formating_date(all_lessons['date'], '-', '.')
        if format_date == sys.argv[1]:
            print('-----------')
            print(format_date)
            print('-----------\n')
            for i in all_lessons['lessons']:
                print(i['time_start'] + ' - ' + i['time_end'])
                print(i['subject'])
                try:
                    print(i['teachers'][0]['full_name'])
                except TypeError:
                    pass
                print(i['auditories'][0]['building']['name'] +
                      ' ' + i['auditories'][0]['name'] + '\n')

    draw_graph(dictionary['lessons']['data'][str(id_group)])


if __name__ == "__main__":
    main()
