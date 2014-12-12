# Jayme Woogerd
# Comp 116 - Security
# December 12, 2014

# This file implements the fuzzy vault algorithm and 
# can be used to create vaults, which encrypt a 
# secret key with a biometric data. The vault can be
# unlocked if presented with a similar enough template.


from random import (uniform, shuffle)
import numpy

degree = 4 # degree 4 polynomial
t = 10     # number of features in each template
r = 40     # number of chaff points

def get_coefficients(word):
    # encodes a secret word as coefficients of a polynomial of 
    # the given degree and returns the coefficients.
    word = word.upper()
    n = len(word) / degree
    if n < 1: n = 1
    substrings = [word[i:i + n] for i in range(0, len(word), n)] 
    coeffs = []
    for substr in substrings:
        num = 0
        for x, char in enumerate(substr):
            num += ord(char) * 100**x
        coeffs.append(num**(1/3.0))
    return coeffs

def p_x(x, coeffs):
    # returns p(x) at the given x, where p(x) is a polynomial function defined 
    # by its coefficients.
    y = 0
    degree = len(coeffs) - 1

    for coeff in coeffs:
        y += x**degree * coeff
        degree -= 1

    return y

def lock(secret, template):
    # given a secret to encode and a biometric template, create and return
    # a fuzzy vault in which this data is encrypted
    vault = []
    coeffs = get_coefficients(secret)

    # calculate genuine points
    for point in template:
        vault.append([point, p_x(point, coeffs)])

    #add chaff points
    max_x = max(template)
    for i in range(t, r):
        x_i = uniform(0, max_x * 1.1)
        y_i = uniform(0, p_x(max_x, coeffs) * 1.1)
        vault.append([x_i, y_i])
    shuffle(vault)
    return vault

def approx_equal(a, b, epsilon):
    return abs(a - b) < epsilon

def unlock(template, vault):
    # given a biometric template and a fuzzy fault, return the coefficients
    # used to encode the secret or None if the template is not a match
    def project(x):
        for point in vault:
            if (approx_equal(x, point[0], 0.001)):
                return [x, point[1]]
        return None

    Q = zip(*[project(point) for point in template if project(point) != None])
    try:
        return numpy.polyfit(Q[0], Q[1], deg=degree)
    except IndexError:
        return None

def decode(coeffs):
    # given a set of coefficients, decode the secret word.
    # decode(get_coefficients(word)) == word
    s = ""
    for c in coeffs:
        num = int(round(c**3))
        if num == 0: continue
        while num > 0:
            s += str(unichr(num % 100)).lower()
            num /= 100
    return s
