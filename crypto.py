from nmath import *

def make_key(key_size,e_size=8):
	prime_length = key_size // 2
	p=get_prime(prime_length)
	q=get_prime(prime_length)
	while p == q:
		q=get_prime(prime_length)

	N=p*q
	ln = calc_lambda(p,q)
	e = calc_e(e_size,ln)
	d = calc_d(e,ln)
	return N, p, q, e, d


def calc_n(prime_length):
	prime_length = prime_length // 2
	p=get_prime(prime_length)
	q=get_prime(prime_length)
	while p == q:
		q=get_prime(prime_length)

	N=p*q
	return p, q, N


def calc_e(prime_length,lambda_n):
	e = get_prime(prime_length)
	coprime = gcd(e,lambda_n)[0]
	while coprime !=1:
		e=get_prime(prime_length)
		coprime=gcd(e,lambda_n)[0]

	return e


def calc_lambda(p,q):
	return lcm(p-1,q-1)


def calc_d(e,lambda_n):
	return mod_inv(e,lambda_n)


def rsa_encrypt(m,e,N):
	return pow(m,e,N)


def rs_decrypt(C,d,N):
	return pow(C,d,N)


def os2ip(os):
	os = os[::-1]
	x = 0
	for i,c in enumerate(os):
		x += (ord(c) *(1<< (8*i)))

	return x


def ip2os(x,x_len):
	if x >= (1<<(8*x_len)):
		raise ValueError("Number is too large to fit in a string of that length")
	X = []
	os = ''
	while x>0:
		X.append(x % 256)
		x >>= 8
	X+=[0]*(x_len-len(X))
	X=X[::-1]
	for item in X:
		os+=chr(item)

	return os


def ascii2ip(string):
	return int(''.join(map(lambda x: str(ord(x)), string)))


def ip2ascii(encoded_num):
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


def make_fermat(bit_width):
	pl = bit_width // 2
	p=get_prime(pl)
	q = next_prime(p+(1<<(pl/8)))
	n = p*q
	ln = calc_lambda(p,q)
	e = calc_e(n & 1 and 9 or 8,ln)
	d = calc_d(e,ln)
	return n,p,q,e,d

