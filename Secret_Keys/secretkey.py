"""This script is used to generate a secret key."""

import os

print os.urandom(24).encode('hex')
