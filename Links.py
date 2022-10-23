#!/usr/bin/env python3
# Использовать urlopen, re (2 балла)
# Печать списка переходов в случае успеха и молчание в случае неуспеха (3 балла)
# Переходить только в пределах ru.wikipedia.org и только в статьи (2 балла)
# Не ходить по страницам дважды, не зацикливаться (2 балла)
# Соответствие PEP8 (1 балл)

from urllib.request import urlopen
import requests
import re


def get_content(name):
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """

    url = 'https://ru.wikipedia.org/wiki/' + str(name)
    response = requests.get(url)
    return response.text


def extract_content(page):
    """
    Функция принимает на вход содержимое страницы и возвращает 2-элементный
    tuple, первый элемент которого — номер позиции, с которой начинается
    содержимое статьи, второй элемент — номер позиции, на котором заканчивается
    содержимое статьи.
    Если содержимое отсутствует, возвращается (0, 0).

    """

    if (page):
        begin = page.find("<div id=\"bodyContent\"")
        end = page.find("</tbody>")  # ???
        content_borders = (begin, end)
        return content_borders
    else:
        return (0, 0)


def extract_links(page, begin, end):
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """
    URLs = []
    page = page[begin:end]
    urls = re.findall(r'<a href="(.+?)"', page)
    for url in urls:
        URLs.append(re.sub(r"^([/#])", r'https://ru.wikipedia.org/\1', url))
    return URLs


def find_chain(start, finish):
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """

    page_start = get_content(start)
    links = extract_links(page_start, extract_content(page_start)[0], extract_content(page_start)[1])
    links_transitions = []
    merged_lists = []
    result = []

    name = ''
    while name != finish:
        merged_lists.append(links)
        for url in links:
            if name == finish:
                #перебираем списки списков и ищем путь от start к finish
                links_transitions.reverse()
                merged_lists.reverse()
                searched_link = finish
                for list_links in links_transitions:
                    for links_of_list_links in list_links:
                        for link in links_of_list_links:
                            if link == searched_link:
                                indx_of_link = links_of_list_links.index()
                                indx_of_link_trans = list_links.index()
                                searched_link = merged_lists[indx_of_link_trans][indx_of_link]
                                result.append(link)
                                break
                break

            name = url[url.find("/wiki/") + 6:]
            content = get_content(name)
            pos = 0
            start = content.find('<title>', pos)
            end = content.find('</title>', start)
            name = content[start+7: end-12]

            links_of_links = []
            page = get_content(name)
            links_of_links.append(extract_links(page, extract_content(page)[0], extract_content(page)[1]))

        links_transitions.append(links_of_links)

        #слияние списков
        links = []
        for link in links_of_links:
            links += link
    result.reverse()
    return result

def main():
    pass


if __name__ == '__main__':
    # name = 'хвоя'
    # page = get_content(name)
    # print(extract_content(page))
    # # print (get_content(name))
    # print(extract_links(page, extract_content(page)[0], extract_content(page)[1]))

    #print(find_chain('теорема', 'аксиома'))
    print(find_chain('математика', 'математика (значения)'))
    #print(find_chain('насекомые', ',бабочка'))