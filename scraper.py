import os
import datetime
import requests
import lxml.html as html

HOME_URL = 'https://cambiocolombia.com'

XPATH_LINK_TO_ARTICLE = '//article//div[@class="sc-hsl1be-0 iSBFgw"]/a/@href'
XPATH_TITLE = '//*[@id="page-content"]/article/header/div/div/div/div/div[1]/div/h1/text()'
XPATH_SUMMARY = '//section[@class="sc-1od3j49-1 bEHWLV"]/p[not(@class)]/text()'
XPATH_BODY = '//div[@class="block-text"]/p/descendant-or-self::text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                title = title.replace('\n', '')
                #remove the quotes from the title
                title.replace('\'', '')
                #remove the tabs from the title
                title = title.replace('\t', '')
                #remove the carriage returns from the title
                title = title.replace('\r', '')
                #remove white spaces from the title
                title = title.strip()
                # Note: title is for .txt file and final_title for processing html title
                final_title = title
                #replace the accents from the title
                title = title.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                #replace the accents from the title
                title = title.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
                #remove the question marks and exclamation marks from the title
                title = title.replace('?', '').replace('¿', '').replace('!', '').replace('¡', '')
                #remove the colons, semicolons, commas, dots, parentheses and spaces from the title
                title = title.replace(':', '').replace(';', '').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
                #remove the special characters from the title 
                title = title.replace('%', '').replace('$', '').replace('#', '').replace('@', '').replace('&', '').replace('*', '').replace('+', '').replace('=', '').replace('-', '').replace('_', '').replace('/', '').replace('\\', '').replace('|', '').replace('<', '').replace('>', '').replace('"', '').replace('\'', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(final_title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():

    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            links_to_notices = ['https://cambiocolombia.com' + link for link in links_to_notices]
            # print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == "__main__":
    run()