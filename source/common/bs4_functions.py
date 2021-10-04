from bs4 import BeautifulSoup


def list_all_elements_to_parse(html_page):
    soup = BeautifulSoup(html_page, 'html.parser')

    list_of_element_type = ['h1', 'div', 'span', 'input']

    for x in range(len(list_of_element_type)):
        current_element_type = list_of_element_type[x]

        all_results = soup.find_all(current_element_type)

        """for i in range(len(all_results)):
            print(all_results[i].attrs,all_results[i].text)"""

        for i in range(len(all_results)):
            copy_element = "element_name = soup.find('" + str(current_element_type) + \
                           "'," + str(all_results[i].attrs) + ").text"

            test = soup.find(current_element_type, all_results[i].attrs).text
            print(test, ' || ', copy_element)

        print('\n\n')


def make_soup(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def make_soup_decode(html,encoding):
    soup = BeautifulSoup(html.content,"html.parser",from_encoding=encoding)
    return soup
