import requests
import hashlib
import random
import string
import json


class Client():
    
    '''
    This module allows human and algorithmic traders to create immutables proofs of their trading performance.\n
    The Proof-of-ROI protocol uses a commit-reveal scheme to ensure that the valuable signals are only publicly verifiable once they lost their value.

    Dependencies:
        * requests
        * hashlib

    \n
    Usage:
        At the moment the signal is created call the `commit` or the `commit_encrypted` method and provide the required data.

        After enougth time is passed and the signal has lost its value call the `reveal` or `reveal_encrypted`method.

    Examples:
        Example of how the Module is used can be found at:\n
        `test.py`

    '''

    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def open_commits(self) -> dict:
        ''' Gets a list of all commits that have not yet been revealed

        Returns:
            a JSON object in format { 
                'list': the list of dicts with commited data,\n
                'message': 'Success' | error_message 
            }
        '''

        url_open_commits = self.base_url + "open_commits"

        header = {
            "X-API-KEY": self.api_key
        }

        r = requests.get(url_open_commits, headers=header)

        return r.json()

    def commit(self, signal: str, price_open: str, exchange: str, time_open: str) -> dict:
        ''' Sends the data to be hashed and commited, data is stored on server for later reveal.

        Args:
            signal (str): the signal either BUY, SELL or STOP
            price_open (str): the price at which the trade was opend
            exchange (str): the exchange on which the trade was executed
            time_open (str): the time at which the trade was opend, compatible with https://pypi.org/project/dateparser/

        Returns:
            a JSON object in format { 
                'tx_hash': the transaction identifier from the Ethereum Blockchain,\n
                'message': 'Success' | error_message 
            }
        '''

        if signal != "BUY" and signal != "SELL" and signal != "STOP":
            return {'message': 'Needs to be one of BUY, SELL, STOP'}

        url_commit_normal = self.base_url + "commit"

        header = {
            "X-API-KEY": self.api_key
        }

        data = {
            "signal": signal,
            "price": str(price_open),
            "exchange": exchange,
            "datetime": time_open
        }

        r = requests.post(url_commit_normal, headers=header, data=data)

        return r.json()

    def reveal(self, index=0) -> dict:
        ''' Reveals a previous commit by publishing its data, default is index 0 (oldes commit).

        Args:
            index (int, default=0): the index of where the commit is in the list returned by `open_commits`

        Returns:
            a JSON object in format {
                'tx_hash': the transaction identifier from the Ethereum Blockchain,\n
                'message': 'Success' | error_message 
            }
        '''

        url_reveal = self.base_url + "reveal"

        header = {
            "X-API-KEY": self.api_key
        }

        data = {
            "api_key": self.api_key,
            "index": index
        }

        r = requests.post(url_reveal, headers=header, data=data)

        return r.json()

    def commit_encrypted(self, signal: str, price_open: str, exchange: str, time_open: str) -> (str, dict):
        ''' Encrypts and sends the data to be commited. Encrypted message is stored on server for later reveal.

        Args:
            signal (str): the signal either BUY, SELL or STOP
            price_open (str): the price at which the trade was opend
            exchange (str): the exchange on which the trade was executed
            time_open (str): the time at which the trade was opend, compatible with https://pypi.org/project/dateparser/

        Returns:
            the encryption key used to generated the encrypted hash 
            a JSON object in format {
                'tx_hash': the transaction identifier from the Ethereum Blockchain,\n
                'index': position of where in the commit list it was stored IMPORTANT: this might change when reveals are made, use `open_commits` instead\n
                'message': 'Success' | error_message 
            }
        '''

        if signal != "BUY" and signal != "SELL" and signal != "STOP":
            return {'message': 'Needs to be one of BUY, SELL, STOP'}


        url_commit = self.base_url + "commit_encrypted"

        header = {
            "X-API-KEY": self.api_key
        }

        encryption_key = "".join(random.choice(string.ascii_uppercase + string.digits) for i in range(20))
        obj = {
            "encryption_key": encryption_key,
            "signal": signal,
            "price": str(price_open),
            "exchange": exchange
        }

        dataBytes = json.dumps(obj)
        message = hashlib.sha256(dataBytes.encode()).hexdigest()

        data = {
            "datetime": time_open,
            "message": message
        }

        r = requests.post(url_commit, headers=header, data=data)

        response = r.json()

        return encryption_key, response

    def reveal_encrypted(self, encryption_key: str, signal: str, price_open: str, exchange: str, time_open: str, index=0):
        ''' Reveals and encrypted commit by publishing the cleartext data, default is index 0 (oldes commit).

        Args:
            encryption_key (str): the key returend by `commit_encrypted`
            signal (str): the signal either BUY, SELL or STOP
            price_open (str): the price at which the trade was opend
            exchange (str): the exchange on which the trade was executed
            time_open (str): the time at which the trade was opend, compatible with https://pypi.org/project/dateparser/
            index (int, default=0): the index of where the commit is in the list returned by `open_commits`

        Returns:
            a JSON object in format { 
                'tx_hash': the transaction identifier from the Ethereum Blockchain,\n
                'message': 'Success' | error_message 
            }
        '''

        if signal != "BUY" and signal != "SELL" and signal != "STOP":
            return {'message': 'Needs to be one of BUY, SELL, STOP'}

        url_reveal_encr = self.base_url + "reveal_encrypted"

        header = {
            "X-API-KEY": self.api_key
        }

        data = {
            "index": index,
            "encryption_key": encryption_key,
            "signal": signal,
            "price": str(price_open),
            "exchange": exchange,
            "datetime": time_open
        }

        r = requests.post(url_reveal_encr, headers=header, data=data)

        return r.json()
