class Blockchain():
    # Produce hash of each block with 4 zeros in the beginning
    difficulty = 4

    def __init__(self, chain=[]):
        self.chain = chain

    def add_block(self, block):
        self.chain.append(block)

    def remove_block(self, block):
        self.chain.remove(block)

    def mining(self, block):
        try:
            block.hash_previous = self.chain[-1].hash()
        except IndexError:
            # THis will set the value of hash_previous = 000000... as we previously defined
            pass
        while True:
            if block.hash()[:self.difficulty] == "0"*self.difficulty:
                self.add_block(block)
                break
            else:
                block.nonce += 1

    def isValid(self):
        for i in range(1, len(self.chain)):
            _previous_hash = self.chain[i].hash_previous
            # Create a new hash for previous block
            _current_hash = self.chain[i-1].hash()
            # Return INVALID if both hashesh do not match and if it does not contain declared number of zeros in the beiginning
            if _previous_hash != _current_hash or _current_hash[:self.difficulty] != "0"*self.difficulty:
                return False

        return True
