from block import Block
from chain import Blockchain

def main():
    blockchain = Blockchain()
    database = ["Hello", "There", "How you doing?"]

    num = 0
    for data in database:
        num += 1
        blockchain.mining(Block(data, num))

    for block in blockchain.chain:
        print(block)

    print(blockchain.isValid())

if __name__ == '__main__':
    main()
