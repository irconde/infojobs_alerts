import requests
from bs4 import BeautifulSoup
import json
import io
import codecs

class GalejobsHandler:

    def __init__(self, config_file):

        self.base_url = 'http://www.galejobs.com'
        self.jobs_list_url = '/empleo'
        self.config_file = config_file
        self.id_max = -1
        self.new_id_max = -1
        self.keyword_list = []
        self.offer_list = []
        self.json_data = None

    def load_config(self):

        input_file = file(self.config_file, "r")
        self.json_data = json.loads(input_file.read().decode("utf-8-sig"))

        self.id_max = int(self.json_data['galejobs']["last_id"])
        self.new_id_max = self.id_max
        self.keyword_list = self.json_data['galejobs']["keywords"]

    def job_is_interesting(self, title):

        is_interesting = False
        num_keywords = len(self.keyword_list)
        index = 0

        while index < num_keywords and not is_interesting:
            if self.keyword_list[index].upper() in title:
                is_interesting = True
            index += 1

        return is_interesting

    def query_job_offers(self):

        if self.keyword_list is not None:

            page = requests.get(self.base_url + self.jobs_list_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            job_offers = soup.find_all('a', class_='ofertas')

            for job_offer in job_offers:

                link = self.base_url + job_offer['href']
                _id = int(link.split('_')[-1])
                offer = {}

                if _id > self.id_max:

                    original_string = job_offer.get_text()
                    string_parts = original_string.split('\n')

                    title = string_parts[2]
                    location = string_parts[6]
                    salary = string_parts[8]
                    date = string_parts[3].split('.')[0]

                    if self.job_is_interesting(title):

                        offer['title'] = title
                        offer['location'] = location
                        offer['salary'] = salary
                        offer['published'] = date
                        offer['link'] = link

                        self.offer_list.append(offer)

                        if _id > self.new_id_max:
                            self.new_id_max = _id

            self.json_data['galejobs']["last_id"] = str(self.new_id_max)

            output_file = codecs.open(self.config_file, "w", encoding="utf-8")
            json.dump(self.json_data, output_file, indent=4, sort_keys=True, ensure_ascii=False)


    def get_offers_summary(self):

        summary = u""

        for offer in self.offer_list:

            title = offer['title']

            summary += title
            summary += "\n"
            summary += offer['link']
            summary += "\n"
            summary = summary + "Salario: " + offer['salary']
            summary += "\n"
            summary = summary + "Ubicacion: " + offer['location']
            summary += "\n"
            summary = summary + "Publicacion: " + offer['published']
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

            summary += title
            summary += "\n"
            summary += offer['link']
            summary += "\n"
            summary = summary + "Salario: " + offer['salary']
            summary += "\n"
            summary = summary + "Ubicacion: " + offer['location']
            summary += "\n"
            summary = summary + "Publicacion: " + offer['published']

            summary_list.append(str(summary.encode('utf-8')))

        return summary_list










