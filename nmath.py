from math import ceil
from random import random, getrandbits


def powmod(b:int,e:int,m:int) -> int:
	"""
	Function to calculate b^e % m using the binary squaring exponation method. Barely slower than CPython native version.

	:param b: Base number
	:param e: Exponent
	:param m: Modulus
	:return: Integer
	"""
	if m == 1:
		return 0
	else:
		r = 1
		while e > 0:
			if e & 1:
				r = (r*b) % m
			e >>= 1
			b = (b*b) % m
		return r


def __pow(b: int, e: int) -> int:
	"""
	reimplementation of the pow function without modulus. Don't use. Internal only.

	:param b: Base
	:param e: Exponent
	:return: Integer result
	"""
	if e == 0: return 1
	r = 1
	while e > 0:
		if e & 1:
			r *= b

		e >>= 1
		b *= b

	return r


def pow(b: int, x: int, m: int = None) -> int:
	"""
	Re-implementation of the CPython pow function for MicroPython.
	Modulus is optional and also handles negative exponents.

	:param b: Base
	:param x: Exponent
	:param m: Modulus.
	:return: Integer or Float if x is positive or negative respectively.
	"""
	res = 0
	if type(x) is not int:
		raise ValueError("exponent must be an integer")
	if m is not None:
		if x > 0:
			res = powmod(b,x,m)
		else:
			res = 1/powmod(b,x*-1,m)
	else:
		if x > 0:
			res = __pow(b, x)
		else:
			res = 1/pow(b,x*-1)

	return res


## recursive version shouldn't really be used to due to stack recursion limits and also stack use.
def __pow_(x: int, y: int, n=None) -> int:
	"""
	Recursive version of the above functions.
	Shouldn't be utilized due to the fact of recursion limits and stack use.

	:param x: number
	:param y: exponent
	:param n: modulus
	:return: Result
	"""
	if y == 0: return 1
	if  y &1 == 0:
		if n is not None:
			return (__pow_(x,(y>>1),n) **2) % n
		else:
			return __pow_(x,(y>>1)) **2
	else:
		if n is not None:
			return (x*__pow_(x,(y-1),n)) % n
		else:
			return x*__pow_(x,(y-1))


def is_square(n: int) -> bool:
	"""
	checks if the number 'n' is an even square.

	:param n: Number to check
	:return: True or False if number is square or not.
	"""
	sq_mod256 = (1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,
	             0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,
				 0,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,
				 0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,
				 0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,
				 0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,
				 0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,
				 1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,
				 0,1,0,0,0,0,0,0)

	if sq_mod256[n & 0xff] == 0:
		return False

	mt = (
		(9, (1,1,0,0,1,0,0,1,0)),
		(5, (1,1,0,0,1)),
		(7, (1,1,1,0,1,0,0)),
		(13, (1,1,0,1,1,0,0,0,0,1,1,0,1)),
		(17, (1,1,1,0,1,0,0,0,1,1,0,0,0,1,0,1,1))
	)
	a = n % 69615
	if any(t[a % m] == 0 for m, t in mt):
		return False

	return int_sqrt(n) ** 2 == n


def int_sqrt(n: int) -> int:
	"""
	Square root function with integers.

	:param n: The integer to work upon.
	:return: An integer resulting from the square root. Just the integer part.
	"""
	if n == 0:
		return 0

	x = 1 << ((n.bit_length() + 1) >> 1)
	while True:
		y = (x + n // x) >> 1
		if y >= x:
			return x
		x = y


def gcd(a:int,b:int) -> tuple:
	"""
	GCD function utilizing EGCD method.

	:param a: First number to check.
	:param b: Second number to check.
	:return: A tuple containing the GCD, and coeffecients a and b.
	"""
	#if a or b is zero return the other value and the coefficients accordingly.
	if a==0:
		return b, 0, 1
	elif b==0:
		return a, 0, 1
	#otherwise actually perform the calculation.
	else:
		#set the gcd x and y according to the outputs of the function.
		# a is b (mod) a. b is just a.
		g, x, y = gcd(b % a, a)
		# we're returning the gcd, x equals y - floor(b/a) * x
		# y is thus x.
		return g, y - (b // a) * x, x


def mod_inv(a:int,mod:int) -> int:
	"""
	Modular inverse calculation using egcd to calculate bezout's coeffecients.

	:param a: Integer to work with.
	:param mod: Modulus value.
	:return: The integer represneting the modular multiplicative inverse.
	"""
	g, x, y = gcd(a,mod)
	if g not in (-1,1):
		raise ValueError('Inputs are invalid. No modular multiplicative inverse exists between {} and {} gcd:{}.\n'.format(a,mod,g))
	else:
		return x % mod


def lcm(a:int,b:int) -> int:
	"""
	Simple LCM function utilizing egcd.

	:param a: The first number.
	:param b: The second number.
	:return: The least common multiple between a and b.
	"""
	if a==0 or b==0:
		return 0
	elif a==1:
		return b
	elif b==1:
		return a

	g=gcd(a,b)[0]
	l=(a//g)*b
	return l


def miller_rabin_base2(n:int) -> bool:
	"""
	Miller Rabbin test for Base 2 only.

	:param n: Integer to check.
	:return: If the number is prime or not.
	:rtype: bool
	"""
	d = n-1
	s = 0
	while not d & 1:
		d >>= 1
		s +=1
	x = pow(2,d,n)
	if x == 1 or x == (n-1):
		return True
	for i in range(s-1):
		x = pow(x,2,n)
		if x == 1:
			return False
		elif x == n -1:
			return True

	return False


def jacobi(a:int,n:int) ->int:
	"""
	Jacobi symbol calculator.

	:param a: The parameter a
	:param n: The parameter n
	:return: The integer
	"""
	if (not n & 1) or (n<0):
		raise ValueError('n must be a positive odd number')
	if(a == 0) or (a == 1):
		return a

	a = a % n
	t = 1
	while a != 0:
		while not a & 1:
			a >>= 1
			if n & 7 in (3,5):
				t = -t
		a, n = n,a
		if (a & 3 == 3) and (n & 3) == 3:
			t = -t
		a %= n
	if n == 1:
		return t

	return 0


def _choose_d(n:int) -> int:
	"""
	D value chooser for lucas psuedoprime test.

	:param n: number to work with.
	:return: the integer value of D.
	"""
	D = 5
	while jacobi(D,n) != -1:
		D +=2 if D > 0 else -2
		D *= -1

	return D


def uv_subscript(k: int, n: int, U: int, V: int, P: int, Q: int, D: int) -> tuple:
	digits = list(map(int,bin(k)[3:]))

	subscript = 1
	for digit in digits:
		U, V = U*V % n, (pow(V, 2, n) - 2*pow(Q, subscript, n)) % n
		subscript <<= 1
		if digit == 1:
			if not (P*U + V) & 1:
				if not (D*U + P*V) & 1:
					U, V = (P*U + V) >> 1, (D*U + P*V) >> 1
				else:
					U, V = (P*U + V) >> 1, (D*U + P*V + n) >> 1
			elif not (D*U + P*V) & 1:
				U, V = (P*U + V + n) >> 1, (D*U + P*V) >> 1
			else:
				U, V = (P*U + V + n) >> 1, (D*U + P*V + n) >> 1
			subscript += 1
			U, V = U % n, V % n

	return U, V


def lucas_pp(n:int, D:int, P:int, Q:float) -> bool:
	U, V = uv_subscript(n + 1, n, 1, P, P, int(Q), D)

	if U != 0:
		return False

	d = n + 1
	s = 0
	while not d & 1:
		d = d >> 1
		s += 1

	U, V = uv_subscript(n + 1, n, 1, P, P, int(Q), D)

	if U == 0:
		return True

	for r in range(s):
		U, V = (U*V) % n, (pow(V, 2, n) - 2*pow(Q, d*(1<<r), n)) % n
		if V == 0:
			return True

	return False

def sieve_test(n):
	sieve_base = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
		31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
		73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
		127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
		179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
		233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
		283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
		353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
		419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
		467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
		547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
		607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
		661, 673, 677, 683, 691, 701, 709, 719, 727, 733,
		739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
		811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
		877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
		947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013,
		1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
		1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151,
		1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223)

	for prime in sieve_base:
		if n == prime:
			return True
		elif n % prime == 0:
			return False
	return None

def baillie_psw(n: int) ->bool:
	if 4 >= n >= 1:
		return True
	elif not n &1:
		return False

	res = sieve_test(n)
	if res is not None:
		return res

	if not miller_rabin_base2(n):
			return False
	elif is_square(n):
		return False

	D = _choose_d(n)
	if not lucas_pp(n,D,1,(1-D)/4):
		return False

	return True


def is_prime(n:int)->bool:
	return baillie_psw(n)


def next_prime(n:int) -> int:
	if n < 2:
		return 2
	if n < 5:
		return (3,5,5)[n-2]
	gap = (1, 6, 5, 4, 3, 2, 1, 4, 3, 2, 1, 2, 1, 4, 3, 2, 1, 2, 1, 4, 3, 2, 1,6, 5, 4, 3, 2, 1, 2)
	n+= 1 if not n &1 else 2
	found_prime = False
	while not found_prime:
		n += gap[n % 30]
		#first do the sieve test as it's fastest.
		tmp = sieve_test(n)
		if tmp is not None:
			found_prime = tmp
		#if it says not conclusive see if the number is a square.
		elif is_square(n):
			found_prime = False
		else:
			#otherwise we do the miller rabin base 2 test.
			if miller_rabin_base2(n):
				#it seems to be prime so try the lucas probable prime test also to make sure.
				D = _choose_d(n)
				if not lucas_pp(n, D, 1, (1 - D) / 4):
					found_prime = False
				#it passed all of the tests so it's probably a prime.
				else:
					break

	return n


def get_prime(bits:int) -> int:
	n = (bits // 31)
	k = 0
	d = 0
	while k < n:
		d|= (getrandbits(31) << (k*31))
		k+=1
	#add the final bit of bits based upon the remainder.
	d |= (getrandbits(bits % 31) << (k*31))
	#then get the next prime number.
	return next_prime(d)