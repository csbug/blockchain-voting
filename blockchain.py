import hashlib
import json
import time


class Block:
    def __init__(self, index, timestamp, votes, previous_hash, nonce=0, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.votes = votes
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash or self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "votes": self.votes,
                "previous_hash": self.previous_hash,
                "nonce": self.nonce,
            },
            sort_keys=True,
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": self.votes,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }


class Blockchain:
    difficulty = 4

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, time.time(), [], "0")
        genesis.nonce = self.proof_of_work(genesis)
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    @staticmethod
    def proof_of_work(block):
        block.nonce = 0
        while True:
            computed = block.compute_hash()
            if computed.startswith("0" * Blockchain.difficulty):
                return block.nonce
            block.nonce += 1

    def add_block(self, votes):
        previous_block = self.chain[-1]
        new_block = Block(
            index=previous_block.index + 1,
            timestamp=time.time(),
            votes=votes,
            previous_hash=previous_block.hash,
        )
        self.proof_of_work(new_block)
        new_block.hash = new_block.compute_hash()
        self.chain.append(new_block)
        return new_block

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.hash:
                return False
            if current.hash != current.compute_hash():
                return False
            if not current.hash.startswith("0" * self.difficulty):
                return False
        return True
