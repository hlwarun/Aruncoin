from hash import updatehash

class Block():
    def __init__(self, number=0, nonce=0, hash_previous='0'*64, data=None):
        # NUMBER is the block number
        self.number = number
        # NONCE is an arbitrary number and comes into play when we use proof-of-work in mining
        self.nonce = nonce
        # DATA consists of the collection of transactions
        # Hash code of previous Block
        # We set its value to 000... because first block has no hash_previous
        # 0 is repeated 64 times because sha256 hashes have length of 64 characters
        self.hash_previous = hash_previous
        self.data = data

    def hash_current(self):
        return updatehash(self.data, self.nonce, self.hash_previous, self.number)

    def __str__(self):
        return str("Block Number: %s\nNonce: %s\nPrevious Block's Hash: %s\nCurrent Block's Hash: %s\nData: %s\n" %(
                    self.number, self.nonce, self.hash_previous, self.hash_current(), self.data))
