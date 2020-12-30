from typing import Tuple
from nmath import *

def make_key(key_size:int,e_size:int=8) -> Tuple[int, int, int, int, int]:
	if key_size & 1:
		prime_length = (key_size//2) + 1
	else:
		prime_length = key_size // 2
	p = get_prime(key_size//2)
	q = get_prime(prime_length)
	while p == q:
		q=get_prime(prime_length)

	N=p*q
	ln = calc_lambda(p,q)
	e = calc_e(e_size,ln)
	d = calc_d(e,ln)
	return N, p, q, e, d


def calc_n(prime_length:int) -> Tuple[int, int, int]:
	if prime_length & 1:
		prime_length = (prime_length//2) + 1
		p = get_prime(prime_length-1)
	else:
		prime_length = prime_length // 2
		p = get_prime(prime_length)

	q=get_prime(prime_length)
	while p == q:
		q=get_prime(prime_length)

	N=p*q
	return p, q, N


def calc_e(prime_length: int, lambda_n: int) -> int:
	e = get_prime(prime_length)
	coprime = gcd(e,lambda_n)[0]
	while coprime !=1:
		e=get_prime(prime_length)
		coprime=gcd(e,lambda_n)[0]

	return e


def calc_lambda(p:int,q:int):
	return lcm(p-1,q-1)


def calc_d(e:int,lambda_n:int):
	return mod_inv(e,lambda_n)


def rsa_encrypt(m,e,N):
	return pow(m,e,N)


def rs_decrypt(C,d,N):
	return pow(C,d,N)


def os2ip(os:str) -> int:
	os = os[::-1]
	x = 0
	for i,c in enumerate(os):
		x += (ord(c) *(1<<(8*i)))

	return x


def ip2os(x:int,x_len:int)->str:
	if x >= (1<<(8*x_len)):
		raise ValueError("Number is too large to fit in a string of that length")
	X = []
	os = ''
	while x>0:
		X.append(x % 256)
		x >>= 8
	X+=([0]*(x_len-len(X)))
	X=X[::-1]
	for item in X:
		os+=chr(item)

	return os


def ascii2ip(string:str) -> int:
	return int(''.join(map(lambda x: str(ord(x)), string)))


def ip2ascii(encoded_num:int) -> str:
	encoded_num = str(encoded_num)
	in_len = len(encoded_num)
	j = 0
	tmp = ''
	output_str = ''
	while j <= in_len-2:
		tmp = encoded_num[j]
		chars = tmp == '1' and 3 or 2
		tmp = encoded_num[j:j+chars]
		output_str += chr(int(tmp))
		j+= chars

	return output_str


def common_mod_atk(c1: int, c2: int, e1: int, e2: int, N: int) -> int:
	a=0;b=0;mx=0;my=0;i=0

	g = gcd(e1,e2)[0]
	if g != 1:
		raise ValueError("e1 and e2 aren't valid. Must be coprimes.")

	a = mod_inv(e1,e2)
	b = (g - (e1*a)) // e2
	i = mod_inv(c2,N)
	mx = pow(c1,a,N)
	my = pow(i,-b,N)

	return (mx*my) % N


def fermats_factor(n:int) -> Tuple[int,int]:
	a = int_sqrt(n)
	b = (a*a) - n
	while not is_square(b):
		a+=1
		b = (a*a) - n

	tmp = int_sqrt(b)
	p = a + tmp
	q = a - tmp
	return p,q


def make_fermat(bit_width:int) -> Tuple[int, int, int, int, int]:
	pl = bit_width // 2
	p=get_prime(pl)
	q = next_prime(p+(1<<(pl//3)))
	n = p*q
	ln = calc_lambda(p, q)
	e = calc_e(n & 1 and 9 or 8, ln)
	d = calc_d(e,ln)
	return n, p, q, e, d

