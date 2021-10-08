comment_list = []
password_hash = "4f1a9e1058dd06089804da225f66f433859138e42c204856b2903fd8181dfea6"

# For password protection

from hashlib import sha256
def create_hash(password):
    pw_bytestring = password.encode()
    return sha256(pw_bytestring).hexdigest()

# Borrowed code. See the original:
# https://bitbucket.org/damienjadeduff/hashing_example/raw/master/hash_password.py

while True:
    comment = input("Enter your comment: ")
    pass_input = input("Enter the password: ")
    hash_input = create_hash(pass_input)
    if hash_input == password_hash:
        comment_list.append(comment)
        print("Comments:")
        for i in range(0, len(comment_list)):
            print(str(i+1) + ". " + comment_list[i])
    else:
        print("Password incorrect.")
