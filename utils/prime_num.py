"""Generates prime numbers up to a given limit using the Sieve of Eratosthenes algorithm."""

## MODULES ##
import math
import random

## FUNCTIONS ##
def is_prime_trial_div(num):
    """Check if a number is prime using trial division."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def prime_sieve(sieve_size):
    sieve = [True] * sieve_size
    sieve[0] = False
    sieve[1] = False
    for i in range(2, int(math.sqrt(sieve_size)) + 1):
        pointer = i * 2
        while pointer < sieve_size:
            sieve[pointer] = False
            pointer += i
    primes = []
    for i in range(sieve_size):
        if sieve[i] == True:
            primes.append(i)
    return primes

def rabin_miller(num):
    if num % 2 == 0 or num < 2:
        return False
    if num == 3:
        return True
    s = num - 1
    t = 0
    while s % 2 == 0:
        s //= 2
        t += 1
    for trials in range(5):
        a = random.randint(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                v = (v ** 2) % num
                i += 1
    return True

LOW_PRIMES = prime_sieve(100)

def is_prime(num):
    if num < 2:
        return False
    for prime in LOW_PRIMES:
        if num % prime == 0:
            return False
    return rabin_miller(num)

def generate_large_prime(key_size=1024):
    while True:
        num = random.randrange(2 ** (key_size - 1), 2 ** key_size)
        if is_prime(num):
            return num