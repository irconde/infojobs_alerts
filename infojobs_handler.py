

import requests
import json
import datetime

class InfojobsHandler:

    def __init__(self, config_file):

        self.url = 'https://api.infojobs.net/api/1/offer'
        self.auth_data = None
        self.parameters = None
        self.config_file = config_file
        self.offer_list = None

    def load_config(self):

        json_string = open(self.config_file).read()
        json_data = json.loads(json_string)
        self.auth_data = (json_data['auth_data']['client_id'], json_data['auth_data']['client_secret'])
        self.parameters = self.process_query_parameters(json_data['parameters'])


    def process_query_parameters(self, json_data):

        # provinces parameters

        aux_parameters = ()
        for province in json_data['provinces']:
            current_prov = ('province', province)
            aux_parameters = (current_prov,) + aux_parameters

        # keywords parameters

        aux_keyword = "("
        for keyword in json_data['keywords']:
            aux_keyword += keyword + " "
        aux_keyword += ")"

        keywords_tuple = ('q', aux_keyword)
        aux_parameters = (keywords_tuple,) + aux_parameters

        # publish date

        time_window = int(json_data['time-window'])

        date = datetime.datetime.utcnow() - datetime.timedelta(minutes=time_window)
        date = date.replace(microsecond=0)
        date = date.isoformat('T') + 'Z'

        date_tuple = ('publishedMin', date)
        aux_parameters = (date_tuple,) + aux_parameters

        return aux_parameters

    def query_job_offers(self):

        if self.auth_data is not None and self.parameters is not None:

            response = requests.get(self.url, auth=self.auth_data, params=self.parameters)
            response_dic = json.loads(response.content)
            self.offer_list = response_dic['offers']
        else:
            self.offer_list = None

    def get_offers_summary(self):

        summary = u""

        for offer in self.offer_list:

            title = offer['title']

            summary += title
            summary += "\n"
            summary += offer['link']
            summary += "\n"
            summary = summary + "Salario: [" + offer['salaryMin']['value'] + " - " + offer['salaryMax']['value'] + "]"
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
            summary = summary + "Salario: [" + offer['salaryMin']['value'] + " - " + offer['salaryMax']['value'] + "]"
            summary += "\n"
            summary = summary + "Publicacion: " + offer['published']

            summary_list.append(str(summary.encode('utf-8')))

        return summary_list

