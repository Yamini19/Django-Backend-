from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.crypto import constant_time_compare
import hashlib,binascii
from backports.pbkdf2 import pbkdf2_hmac
from django.utils.translation import gettext_noop as _

class CustomHasher(BasePasswordHasher):
    iterations = 10000
    algorithm = "pbkdf2_sha512"
    digest = hashlib.sha512
    desired_keyLength= 32
    custom_salt = 'c38sb91my094ld41'

    def salt(self):
        salt = 'c38sb91my094ld41'
        return salt

    def encode(self, password, salt, iterations=None):
        self._check_encode_args(password, salt)
        iterations = iterations or self.iterations
        hash = pbkdf2_hmac("sha512", password.encode(), self.custom_salt.encode(), iterations,dklen= self.desired_keyLength)
        hash = binascii.hexlify(hash)
        return hash

    def verify(self, password, encoded):
        encoded_2 = self.encode(password, salt=self.salt(), iterations=self.iterations)
        return constant_time_compare(encoded.split("'")[1], encoded_2.decode())

