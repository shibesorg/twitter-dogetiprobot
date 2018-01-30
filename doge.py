"""Dogecoin RPC node interface"""

import dogecoinrpc
from config import (DOGECOIN_USER, DOGECOIN_PASSWORD, DOGECOIN_HOST, DOGECOIN_PORT)


class DogecoinConnection():
    def __init__(self, username, password, host, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        
        try:
            self.conn = dogecoinrpc.connect_to_remote(
                self.username,
                self.password,
                host=self.host,
                port=self.port,
            )
        except Exception as e:
            print(e)
            print('Error could not connect to node.')

    def get_balance(self, account_name):
        return self.conn.getbalance(account_name, minconf=1)

    def get_newaddress(self, account_name):
        return self.conn.getnewaddress(account_name)

    def send_from(self, from_acct, to_addr, amount, comment='Sent from @dogetiprobot'):
        return self.conn.sendfrom(
            from_acct,
            to_addr,
            amount,
            minconf=1,
            comment=comment,
            comment_to=comment,
        )

    def list_transactions(self, account_name):
        return self.conn.listtransactions(account_name, count=10)


dogeconn = DogecoinConnection(
    DOGECOIN_USER,
    DOGECOIN_PASSWORD,
    DOGECOIN_HOST,
    DOGECOIN_PORT,
)
