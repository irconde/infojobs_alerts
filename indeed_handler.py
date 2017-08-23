import json
import requests
from bs4 import BeautifulSoup
import sqlite3


class IndeedHandler:
    def __init__(self, config_file):

        self.base_url = 'http://www.indeed.es'
        self.url_part1 = 'http://www.indeed.es/ofertas?as_and=&as_phr=&as_any='
        self.url_part3 = '&as_not='
        self.url_part5 = '&as_ttl=&as_cmp=&jt=fulltime&st=&radius=100&l='
        self.url_part7 = '&fromage=last&limit=10&sort=date&psf=advsrch'
        self.config_file = config_file
        self.keyword_list = []
        self.locations_list = []
        self.exceptions_list = []
        self.offer_list = []
        self.db_connection = sqlite3.connect('jobs.db')

    def load_config(self):

        input_file = file(self.config_file, "r")
        json_data = json.loads(input_file.read().decode("utf-8-sig"))
        self.locations_list = json_data['indeed']["provinces"]
        self.keyword_list = json_data['indeed']["keywords"]
        self.exceptions_list = json_data['indeed']['exceptions']
        # print self.locations_list[2].encode('utf-8')
        # print self.keyword_list[0].encode('utf-8')

    def wordlist_to_string(self, _list):

        num_keywords = len(_list)
        result_string = ''

        if num_keywords > 0:
            index = 0
            result_string = _list[index]
            index += 1
            while index < num_keywords:
                result_string = result_string + '+' + _list[index]
                index += 1

        return result_string

    def save_to_db(self, offer):

        c = self.db_connection.cursor()

        c.execute("INSERT INTO indeed VALUES ('" +
                                   offer['link'] + "', '" +
                                   offer['title'] + "', '" +
                                   offer['location'] + "', '" +
                                   offer['company'] + "', '" +
                                   offer['published'] + "')")

    def job_is_in_db(self, job_url):

        c = self.db_connection.cursor()

        c.execute("SELECT COUNT(*) FROM indeed WHERE href = '%s'" % job_url)

        num_results = c.fetchone()[0]

        if num_results > 0:
            return True
        else:
            return False


    def query_job_offers(self):

        if self.keyword_list is not None and self.keyword_list is not []:

            keywords_string = self.wordlist_to_string(self.keyword_list)
            exceptions_string = self.wordlist_to_string(self.exceptions_list)

            if self.locations_list is not None and self.locations_list is not []:

                for location in self.locations_list:

                    request_url = self.url_part1 + keywords_string + self.url_part3 + exceptions_string \
                                  + self.url_part5 + location + self.url_part7

                    page = requests.get(request_url)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    results = soup.find_all('div', class_=' row result')

                    for result in results:

                        # Date
                        published = ""
                        aux_published = result.find('span', class_="date")
                        if aux_published is not None:
                            published = aux_published.get_text().rstrip().lstrip()

                        if published == "Publicado ahora":

                            offer = {}

                            link = result.find('a', class_="turnstileLink")['href']
                            offer['link'] = self.base_url + link

                            if not self.job_is_in_db(offer['link']):

                                title = result.find('h2', class_="jobtitle").get_text().rstrip().lstrip()

                                # Company
                                aux_company = result.find('span', class_="company")
                                company = ""
                                if aux_company is not None:
                                    company = aux_company.get_text().rstrip().lstrip()

                                location = result.find('span', class_="location").get_text().rstrip().lstrip()

                                offer['title'] = title
                                offer['location'] = location
                                offer['company'] = company
                                offer['published'] = published

                                self.save_to_db(offer)
                                self.offer_list.append(offer)

        self.db_connection.commit()
        self.db_connection.close()


    def get_offers_summary(self):

        summary = u""

        for offer in self.offer_list:
            title = offer['title']
            summary += title
            summary += "\n"
            summary += offer['link']
            summary += "\n"
            summary = summary + "Publicacion: " + offer['published']
            summary += "\n"
            summary = summary + "Compania: " + offer['company']
            summary += "\n"
            summary = summary + "Lugar: " + offer['location']
            summary += "\n"
            summary += "\n"
            summary += "-----------------------------------------------------------------------------------------------"
            summary += "\n"
            summary += "\n"

        return summary.encode('utf-8')

    def get_offers_list(self):

        summary_list = []

        for offer in self.offer_list:
            summary = u""

            title = offer['title']

            title = offer['title']
            summary += title
            summary += "\n"
            summary += offer['link']
            summary += "\n"
            summary = summary + "Publicacion: " + offer['published']
            summary += "\n"
            summary = summary + "Compania: " + offer['company']
            summary += "\n"
            summary = summary + "Lugar: " + offer['location']

            summary_list.append(str(summary.encode('utf-8')))

        return summary_list