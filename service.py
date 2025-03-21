import random
import string

# Function to generate a unique short code
def generate_short_code(length=6):
    code_string = ''.join(random.choices(string.ascii_letters, k=length//2))
    code_num = ''.join(random.choices(string.digits, k=length//2))
    short_code = code_string + code_num
    return short_code
