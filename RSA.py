import random
from math import gcd
from sympy import isprime

def generate_prime_candidate(length):
    """Berilgan uzunlikda tub son nomzodini yaratish"""
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1  # Eng yuqori va eng past bitlarni 1 qilish
    return p

def generate_prime_number(length):
    """Berilgan uzunlikda tub son generatsiya qilish"""
    p = 4
    while not isprime(p):
        p = generate_prime_candidate(length)
    return p

def extended_gcd(a, b):
    """Kengaytirilgan Evklid algoritmi"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """Modul inversiyani hisoblash"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def generate_keys(bit_length):
    """Ochiq va yopiq kalitlarni generatsiya qilish"""
    # Ikkita katta tub son generatsiya qilish
    p = generate_prime_number(bit_length)
    q = generate_prime_number(bit_length)
    
    while p == q:
        q = generate_prime_number(bit_length)
    
    # n ni hisoblash
    n = p * q
    
    # Euler funktsiyasi φ(n) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)
    
    # e ni tanlash (odatda 65537)
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    # d ni hisoblash (e ning mod φ(n) dagi inversiyasi)
    d = modinv(e, phi)
    
    # Ochiq kalit: (e, n), yopiq kalit: (d, n)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    """Matnni shifrlash"""
    e, n = public_key
    # Har bir belgini ASCII kodiga o'tkazib, keyin shifrlash
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    """Shifrlangan matnni ochish"""
    d, n = private_key
    # Har bir shifrlangan blokni ochib, keyin ASCII belgiga o'tkazish
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

if __name__ == "__main__":
    print("RSA Shifrlash Algoritmi")
    print("Kalitlar generatsiya qilinmoqda...")
    
    # Kalitlarni generatsiya qilish (128 bit)
    public_key, private_key = generate_keys(128)
    
    print(f"\nOchiq kalit (e, n): {public_key}")
    print(f"Yopiq kalit (d, n): {private_key}")
    
    # Shifrlash uchun matn
    message = "Salom Dunyo! 123"
    print(f"\nOriginal xabar: {message}")
    
    # Xabarni shifrlash
    encrypted_msg = encrypt(public_key, message)
    print(f"Shifrlangan xabar: {encrypted_msg}")
    
    # Shifrlangan xabarni ochish
    decrypted_msg = decrypt(private_key, encrypted_msg)
    print(f"Ochilgan xabar: {decrypted_msg}")
