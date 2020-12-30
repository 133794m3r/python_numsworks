from crypto import *
from nmath import *
p, q, N, d, e, ct = 0, 0, 0, 0, 0, 0
def get_int(prefix):
	while True:
		try:
			ans = input(prefix)
			if ans[0:2] == "0x":
				num = int(ans,16)
			elif ans[0:2] == "0b":
				num = int(ans,2)
			else:
				num = int(ans)
			break
		except ValueError:
			print("Provide a valid number.")

	return num

def get_opt(prefix,m,n):
	while True:
		try:
			ans = int(input(prefix))
			if n >= ans >= m:
				break
			else:
				print("Enter a valid option.")
		except ValueError:
			print("Enter a valid number.")
	return ans

def get_params(decrypt=False):
	p = get_int("Enter p: ")
	q = get_int("Enter q: ")
	N = p*q
	e = 1
	if decrypt:
		d = get_int("Enter d: ")
	else:
		e = get_int("Enter e: ")
		d = mod_inv(e,calc_lambda(p,q))

	return N, p, q, e, d

def rsa_encrypt_str():
	global p, q, N, d, e, ct
	options = [ascii2ip,os2ip]

	params_provided = get_opt("1) Provide parameters.\n2) Generate parameters.\n", 1, 2)

	opt = get_opt("Select Encoding\n1) Ascii String\n2) Standard RSA\n",1,2)

	pt = input("Enter Plaintext: ")
	M = options[opt](pt)
	#this should be enough to make sure that the prime N is larger than M due to the fact that
	#p and q are both half the size so the prime we get could be smaller than M which would be disastrous.
	bits = ceil((bit_len(M)+1)*1.22)
	if bits >= 64:
		e_len = 32
	elif bits >= 32:
		e_len = 16
	else:
		e_len = 8
	if params_provided == 2:
		N, p, q, e, d = make_key(bits, e_len)
	else:
		N, p, q, e, d = get_params()
	ct = pow(M, e, N)
	print('m={}'.format(hex(M)))
	print('p={},q={},N={},e={},d={}'.format(hex(p), hex(q), hex(N), hex(e), hex(d)))
	print('ct={}'.format(hex(pow(M, e, N))))


def rsa_decrypt_str():
	params_provided = get_opt("1) Provide parameters.\n2) Use Previous Values\n", 1, 2)
	opt = get_opt("Select Encoding\n1) Ascii String\n2) Standard RSA\n",1,2)
	options = [ip2ascii,ip2os]
	if params_provided == 2:
		global p, q, N, e, d, ct
	else:
		N, p, q, e, d  = get_params(True)
		ct = get_int("Enter Ciphertext Integer: ")


	C = pow(ct,d,N)
	ct_len = ceil(bit_len(C)/8)
	print("Decrypted Message: ", options[opt](C,ct_len),"\n\n")


def fermat_attack():
	pass

def common_mod_attack():
	pass


def main():
	options = [rsa_encrypt_str,rsa_decrypt_str,fermat_attack,common_mod_attack]
	while True:
		#print("Select Option\n1) RSA Encrypt\n2) RSA Decrypt\n3) Fermat Attack Generator/Solver\n4) Common Modulus Attack Generator/Solver\n5) Exit\n")
		ans = get_opt("Select Option\n1) RSA Encrypt\n2) RSA Decrypt\n3) Fermat Attack Generator/Solver\n4) Common Modulus Attack Generator/Solver\n5) Exit\n",1,5)
		if 4 >= ans >= 1:
			options[ans-1]()
		elif ans == 5:
			break




if __name__ == "__main__":
	main()