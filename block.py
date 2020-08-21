from hash import updatehash

class Block():
    # DATA consists of the collection of transactions
    data = None
    # HASH is the hash code of transactions
    hash = None
    # NONCE is an arbitrary number and comes into play when we use proof-of-work in mining
    nonce = 0
    # Hash code of previous Block
    # We set its value to 000... because first block has no hash_previous
    # 0 is repeated 64 times because sha256 hashes have length of 64 characters
    hash_previous = '0'*64

    def __init__(self, data, number=0):
        self.data = data
        # NUMBER is the block number
        self.number = number

    def hash(self):
        return updatehash(self.data, self.nonce, self.hash_previous, self.number)

    def __str__(self):
        return str("Block Number: %s\nPrevious Block's Hash: %s\nCurrent Block's Hash: %s\nData: %s\nNonce: %s\n" %(
                    self.number, self.hash_previous, self.hash(), self.data, self.nonce))
