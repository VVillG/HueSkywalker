from passlib.hash import sha256_crypt
salt = "password3"

pass1 = "password1"
pass2 = "password2"

saltpass1 = pass1 + salt
saltpass2 = pass2 + salt

newpass1 = sha256_crypt.encrypt(saltpass1)
newpass2 = sha256_crypt.encrypt(saltpass2)

print(newpass1)
print(newpass2)

print(sha256_crypt.verify("password1"+salt, newpass1))
