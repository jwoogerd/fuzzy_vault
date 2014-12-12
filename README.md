### Fuzzy Vault Implementation

This code implements a very simple "biometric" authentication system using the
fuzzy vault algorithm as described by Juels and Sudan in 
[*A Fuzzy Vault Scheme*](http://people.csail.mit.edu/madhu/papers/2002/ari-journ.pdf). 
I have made some notable simplifications (in fuzzy_vault.py):

1. The "biometric" data is represented as a list of 
ten floats. Real fingerprint data is more complex.
1. I have simplified the polynomial interpolation -- rather than using 
[Reed-Solomon codes](http://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction), 
I used the a polynomial fit function.
1. Chaff points are not thrown out if they collide with genuine points on 
the polynomial.

To run the program, choose a fingerprint file from the `fingerprints` directory,
e.g. `ming` and run:

    python authenticate.py fingerprints/ming

This program imports a list of vaults, which were created using "fingerprints"
(biometric templates). Each vault stores encrypted fingerprint data bound with a 
secret key (i.e. the name of the person). Thus, when `authenticate.py` is 
invoked with the supplied template, we try to unlock each vault to get the 
name encrypted in it. If the template is a close enough match to the original 
template used to create the vault and the name returned is on a list of known 
users, we get a match and the user is accepted.