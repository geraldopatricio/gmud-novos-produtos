import json
import requests, aiohttp
from dataclasses import dataclass

from .safebox import Safebox

class Pier():
    def __init__(self):
        self.url = Safebox.get_secret('API-PIER-URL')
        #self.url = "http://localhost:5000"
        self.__client_id = Safebox.get_secret('API-PIER-CLIENTID')
        self.__access_token = Safebox.get_secret('API-PIER-TOKEN')
        
        self.__headers = {
            "client_id": self.__client_id,
            "access_token": self.__access_token,
        }
        connector = aiohttp.TCPConnector(limit=100)
        self._client = aiohttp.ClientSession(connector=connector, headers=self.__headers, raise_for_status=True)


    async def close(self) -> None:
        return await self._client.close()

    async def get(self, url, params={}, json={}, headers={}):
        headers = {
            **self.__headers,
            **headers
        }
        resp = await self._client.get(self.url + url, headers=headers, json=json, params=params) 
        return await resp.json()

    async def post(self, url, params={}, json={}, headers={}):
        headers = {
            **self.__headers,
            **headers
        }
        resp = await self._client.post(self.url + url, headers=headers, json=json, params=params)
        return await resp.json()

       