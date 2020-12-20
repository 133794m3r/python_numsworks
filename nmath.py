from random import randint, getrandbits

def is_square(n: int) -> bool:
	sq_mod256 = (1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0)
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
	if n == 0:
		return 0

	x = 1 << ((n.bit_length() + 1) >> 1)
	while True:
		y = (x + n // x) >> 1
		if y >= x:
			return x
		x = y

def gcd(a:int,b:int) -> tuple:
	#if a or b is zero return the other value and the coeffecient's accordingly.
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

def lcm(a:int,b:int) -> int:
	if a==0 or b==0:
		return 0
	elif a==1:
		return b
	elif b==1:
		return a

	g=gcd(a,b)[0]
	l=(a//g)*b
	return l

def uv_subscript(n: int, u1: int, v1: int, u2: int, v2: int, d: int, q: int, m: int) -> tuple:
	k=q
	while m>0:
		u2 = (u2 * v2) % n
		v2 = ((v2 * v2) - (2 * q)) % n
		q = (q*q) % n
		if m & 1:
			t1, t2 = u2*v1, u1*v2
			t3, t4 = v2*v1, u2 * u1 * d
			u1, v1 = t1 + t2, t3+t4
			if u1 &1:
				u1 = u1 + n
			if v1 & 1:
				v1 = v1 +n
			u1, v1 = (u1/2) % n, (v1/2) % n
			k = (q*k) % n
		m = m >> 1

	return u1, v1

def _factor(n:int,p:int=2) -> int:
	s=0;d = n -1; q = p
	while not (d & q -1):
		s +=1
		q *= p
	return s, d // (q // p)

def strong_psuedoprime(n: int, a: int, s: int = None, d: int = None) -> int:
	if (s is None) or (d is None):
		s, d = _factor(n)
	x = pow(a,d,n)
	if x == 1:
		return True

	for i in range(s):
		if x == n -1:
			return True
		x = pow(x,2,n)

	return False

def lucas_psuedoprime(n: int, D: int, P: int, Q: int) -> int:
	U, V = uv_subscript(n+1,n,1,P,P,Q,D)
	if U != 0:
		return False
	d = n+1
	s = 0
	while not d & 1:
		d >>= 1
		s+=1

	U, V = uv_subscript(n+1,n,1,P,P,Q,D)

	if U == 0:
		return True

	for r in range(s):
		u, v = (U*V)%n, (pow(V,2,n) - 2*pow(Q,d*(1<<r),n)) % n
		if V == 0:
			return True

	return False


def jacobi(a:int,n:int) ->int:
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
	D = 5
	while jacobi(D,n) != -1:
		D +=2 if D > 0 else -2
		D *= -1

	return D


def baillie_psw(n: int) ->bool:
	if 4 >= n >= 1:
		return True
	elif not n &1:
		return False

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

	if not strong_psuedoprime(n,2):
		return False

	if is_square(n):
		return False

	D = _choose_d(n)
	if not lucas_psuedoprime(n,D,1,(1-D)/4):
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
	while not is_prime(n):
		n += gap[n % 30]

	return n

def get_prime(bits:int) -> int:
	candidate = getrandbits(bits)
	return next_prime(candidate)