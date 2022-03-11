import json
import requests

from .safebox import Safebox





class Pier():

    def __init__(self):
        #self.url = Safebox.get_secret('API-PIER-URL')
        self.url = "http://localhost:5000"
        self.__client_id = Safebox.get_secret('API-PIER-CLIENTID')
        self.__access_token = Safebox.get_secret('API-PIER-TOKEN')
        self.__headers = {
            "client_id": self.__client_id,
            "access_token": self.__access_token,
            "Content-Type": "application/json",
        }


    def get(self, url, params={}, body={}, headers={}, format_json=False):
        headers = {
            **self.__headers,
            **headers
        }
        result = requests.get(self.url + url, headers=headers, data=body, params=params)
        if result.status_code in [200, 201]:
            if format_json is not False:
                return json.loads(result.content)
            return result.content
        else:
            return False

    def post(self, url, params={}, body={}, headers={}, format_json=False):
        headers = {
            **self.__headers,
            **headers
        }
        result = requests.post(self.url + url, headers=headers, data=body, params=params)
        if result.status_code in [200, 201]:
            if format_json is not False:
                return json.loads(result.content)
            return result.content
        else:
            return False

    def put(self, url, params, body={}, headers={}, format_json=False):
        headers = {
            **self.__headers,
            **headers
        }
        send_url = self.url + url + '?' + self._dict_to_query(params)
        print(send_url)
        result = requests.put(send_url, headers=headers, data=body)
        if result.status_code in [200, 201]:
            print('OPERACAO CONCLUIDA URL: {}'.format(send_url))
            if format_json is not False:
                return json.loads(result.content)
            return result.content
        else:
            print('FALHA NA OPERACAO URL: {}'.format(send_url))
            return False

        
    def _dict_to_query(query_dict: dict):
        query = ''
        for index, key in enumerate(query_dict.keys()):
            if index == len(query_dict.keys()) - 1:
                query += str(key) + '=' + str(query_dict[key])
            else:
                query += str(key) + '=' + str(query_dict[key]) + "&"
        return query
