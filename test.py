import time

from AlphaProof import Client

API_KEY = "QWTI6SY9U1IH823MQJHU"
BASE_URL = "http://127.0.0.1:5000/"

TIME_OPEN = "16:11 CEST"
PRICE_OPEN = str(6725.0)
EXCHANGE = "bitstamp"


def main():

    client = Client(API_KEY, BASE_URL)

    ''' Make cleartext commit-reveal
    '''
    response = client.commit("BUY", PRICE_OPEN, EXCHANGE, TIME_OPEN)
    print("\n" + str(response))
    time.sleep(90)  # wait for transaction to be mined

    response = client.open_commits()
    print("\n" + str(response))

    response = client.reveal(2)
    print("\n" + str(response))
    time.sleep(90)  # wait for transaction to be mined

    ''' Make encrypted commit-reveal
    '''
    encr_key, response = client.commit_encrypted("BUY", PRICE_OPEN, EXCHANGE, TIME_OPEN)
    index = response["index"]
    print("\n" + str(response))
    print("encryption key used: " + str(encr_key))
    time.sleep(90)  # wait for transaction to be mined

    response = client.open_commits()
    print("\n" + str(response))

    response = client.reveal_encrypted(encr_key, "BUY", PRICE_OPEN, EXCHANGE, TIME_OPEN, index)
    print("\n" + str(response))
    time.sleep(90)  # wait for transaction to be mined


if __name__ == "__main__":
    main()
