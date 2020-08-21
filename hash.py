from hashlib import sha256

def updatehash(*args):
    hash_string = ""
    s = sha256()
    for i in args:
        hash_string += str(i)
    s.update(hash_string.encode('utf-8'))
    return s.hexdigest()
