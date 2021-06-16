from backend.wallet.transaction_pool import TransactionPool
from backend.config import STARTIN_BALANCE
from backend.test.blockchain.test_block import block
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.blockchain.blockchain import Blockchain
from backend.config import STARTIN_BALANCE

def test_verify_valid_signature():
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)


    assert Wallet.verify(wallet.public_key, data, signature)

def test_verify_invalid_signature():
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(Wallet().public_key, data, signature)


def test_calculate_balance():

    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTIN_BALANCE
    
    amount = 50
    transaction = Transaction(wallet, 'recipient', amount)
    blockchain.add_block([transaction.to_json()])

    assert Wallet.calculate_balance(blockchain, wallet.address) == \
        STARTIN_BALANCE - amount

    received_amount_1 = 25
    recieved_transaction_1 = Transaction(
        Wallet(),
        wallet.address,
        received_amount_1
    )  
    received_amount_2 = 50
    recieved_transaction_2 = Transaction(
        Wallet(),
        wallet.address,
        received_amount_2
    )      

    blockchain.add_block(
        [recieved_transaction_1.to_json(), recieved_transaction_2.to_json()]
    )

    assert Wallet.calculate_balance(blockchain, wallet.address) == \
        STARTIN_BALANCE - amount + received_amount_1 + received_amount_2




