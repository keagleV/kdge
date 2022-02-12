
import argparse
from kdgeLogger import KdgeLogger
from os import path
from random import randint

from itertools import product
from random import shuffle
from operator import sub


from pickle import dump
from pickle import load

from os import makedirs

class Kdge:

	'''
		This class has implemented the encryption and decryption functionalities
		of the DNA Genetic Encryption
	'''

	def __init__(self):

		# File containing the encryption/decryption key
		self.keyFile = str()

		# File containing the encrypted message
		self.ciphertextFile = str()


		# File containing the plaintext
		self.plaintextFile = str()

		# File containing the key
		self.keyFile = None

		# Ouput directory of the action
		self.outputDir=None

		# Length of the key, default key size is 128
		self.keyLen = 128

		# Encryption Action
		self.encryptionAction = "enc"

		# Decryption Action
		self.decryptionAction = "dec"

		# Logger Handler
		self.logHandler = KdgeLogger()

		# DNA encodings
		self.dnaEncodings = dict()

		# DNA proteins encodings
		self.dnaProEncodings = dict()


		# Message Codes

		self.messCode = {
		'INVALID_ACTION': 'Invalid Action Selected (values: end/dec) ',
		'ENCRYPTION_NOT_ENOUGH_ARGS': 'Plaintext File Not Provided For Encryption',
		'DECRYPTION_NOT_ENOUGH_ARGS': 'Ciphertext File Not Provided For Decryption',
		'PLAINTEXT_FILE_NOT_EXIST': 'Plaintext File Not Exist',
		'KEY_FILE_NOT_EXIST': 'Key File Not Exist',
		'KEY_LENGTH_NOT_SPECIFIED': 'Length Of The Key Should Be Specified',
		'CIPHERTEXT_FILE_NOT_EXIST': 'Ciphertext File Not Exist',
		'ENCRYPTION_NO_ACTION_SPECIFIED': 'No Action Specified',
		'DECRYPTION_NO_KEY_FILE': 'No Key File Has Specified, Decryption Failed'

		}



	def parse_command_arguments(self):

		'''
			This function parses the command line arguments of the program
		'''

		parser = argparse.ArgumentParser(description='Create Configuration File Help')

		parser.add_argument('-p','--pfile',  type=str, nargs=1,help='Specify Plaintext File')
		parser.add_argument('-c','--cfile',  type=str, nargs=1,help='Specify ciphertext File')
		parser.add_argument('-k','--kfile',  type=str, nargs=1,help='Specify key File')
		parser.add_argument('-l','--keylen',  type=str, nargs=1,help='Specify key Length')
		parser.add_argument('-a','--action',  type=str, nargs=1,help='Specify Action')
		parser.add_argument('-e','--ea',  type=str, nargs=1,help='Specify EA Parameters File')
		parser.add_argument('-o','--out',  type=str, nargs=1,help='Specify Output Directory')


		args = parser.parse_args()


		if args.action:

			# Checking for the output directory
			if args.out:
				self.outputDir = args.out[0]

			# Checking for the keyfile since it is independent of the action
			if args.kfile:

				# Check for the length of the key
				if not args.keylen:
					self.logHandler.log_message(self.messCode['KEY_LENGTH_NOT_SPECIFIED'],'ERR')
					exit(1)

				self.keyLen = int(args.keylen[0])
				self.keyFile= args.kfile[0]

			# Action
			action = (args.action[0]).lower()

			if action == self.encryptionAction:

				if not (args.pfile):
					self.logHandler.log_message(self.messCode['ENCRYPTION_NOT_ENOUGH_ARGS'],'ERR')
					exit(1)


				# Check for plaintext file existance
				if not (path.exists(args.pfile[0])):
					self.logHandler.log_message(self.messCode['PLAINTEXT_FILE_NOT_EXIST'],'ERR')
					exit(1)


				# Run encryption
				self.plaintextFile = args.pfile[0]
				
				self.kdge_encrypt()
				


			elif action == self.decryptionAction:
				
				# Check for argument providance
				if not (args.cfile):
					self.logHandler.log_message(self.messCode['CIPHER_NOT_ENOUGH_ARGS'],'ERR')
					exit(1)


				# Check for ciphertext file existence
				if not (path.exists(args.cfile[0])):
					self.logHandler.log_message(self.messCode['CIPHER_FILE_NOT_EXIST'],'ERR')
					exit(1)


				# Run decryption
				self.ciphertextFile = args.cfile[0]
				
				self.kdge_decrypt()



			else:
				self.logHandler.log_message(self.messCode['INVALID_ACTION'],'ERR')
				exit(1)

		else:
			self.logHandler.log_message(self.messCode['ENCRYPTION_NO_ACTION_SPECIFIED'],'ERR')
			exit(1)
			


	def create_dna_alphabet_encoding(self):
		'''
			This function will create a dna-alphabet encondig for all the ascii characters
		'''

		# Since we have 256 possible values in ascii table, we have to create 256 dna encondings
		dnaEncodings = list(product(list('ATCG'), repeat=4))

		# Next we will shuffle the encodings
		shuffle(dnaEncodings)


		for idx, val in enumerate(dnaEncodings):
			self.dnaEncodings[idx]="".join(val)
			


	def create_dna_protein_binaries(self):

		'''
			This function creates a mapping of DNA proteins (A,T,C,G) with binaries 0,1
		'''
		binariesEncodings = list(product(list('01'), repeat=2))


		# Next we will shuffle the encodings
		shuffle(binariesEncodings)
		
		self.dnaProEncodings['A'] = "".join(binariesEncodings[0])

		self.dnaProEncodings['T'] = "".join(binariesEncodings[1])

		self.dnaProEncodings['C'] = "".join(binariesEncodings[2])

		self.dnaProEncodings['G'] = "".join(binariesEncodings[3])



	def kdge_decrypt(self):
		'''
			This function has implemented the decryption function
		'''

		# List of bits of the keyfile
		keyFileBitsList = list()



		# Check for the keyfile existance
		if not self.keyFile:
				self.logHandler.log_message(self.messCode['DECRYPTION_NO_KEY_FILE'],'ERR')
				exit(1)

		# Reading encodings file
		with open("out/alphabet.enc", "rb") as iffile:
			dnaEncodings = load(iffile)

			# Reversing the dictionary for decryption
			self.dnaEncodings =  {y:x for x,y in dnaEncodings.items()}
		

		# Reading protein encodings file
		with open("out/dnaprot.enc", "rb") as iffile:
			dnaProEncodings = load(iffile)

			# Reversing the dictionary for decryption
			self.dnaProEncodings =  {y:x for x,y in dnaProEncodings.items()}


			


		# Reading the keyfile
		fhandle = open(self.keyFile,'rb')
		keyBytes = fhandle.read(100)
		fhandle.close()



		for byte in keyBytes:
			keyFileBitsList += list(bin(byte)[2:].zfill(8))



		# Reading the ciphertext file
		fhandle=open(self.ciphertextFile,'rb')
		lines = fhandle.readlines()
		fhandle.close()


		# Ciphertext binaries of the bytes
		ciphertextFileCharEncoding=list()

		for line in lines:

			for char in line.strip():
				ciphertextFileCharEncoding += list(bin(char)[2:].zfill(8)) 


		# Next, we XOR the cipher text with the given key

		# First, make key and the plaintext equal length
		differenceMul = len(ciphertextFileCharEncoding) // len(keyFileBitsList)
		differenceMod = len(ciphertextFileCharEncoding) % len(keyFileBitsList)
		newKey = keyFileBitsList*differenceMul + keyFileBitsList[:differenceMod]


		# Next level plaintext hols the xor value
		nextLevelPlaintext = []

		for i in range(len(ciphertextFileCharEncoding)):
			
			if ( ciphertextFileCharEncoding[i]=='1' and newKey[i]=='1') or (ciphertextFileCharEncoding[i]=='0' and newKey[i]=='0'):
				nextLevelPlaintext.append('0')
			
			else:
				nextLevelPlaintext.append('1')


		# Next, we group bits 2by2 to translate them to their protein representation
		proteinRepresentation = list()
		for idx in range(0,len(nextLevelPlaintext),2):
			proteinCode = "".join(nextLevelPlaintext[idx:idx+2])

			# Translate the protein code with the protein encoding
			proteinRepresentation.append(self.dnaProEncodings[proteinCode])

		
		# Next, we group proteins 4by4 to translate them to their ascii representation, and finally,
		# we use alphabet encoding to translate the grouped proteins

		asciiRepresentation = list()
		for idx in range(0,len(proteinRepresentation),4):
			groupedProteins = "".join(proteinRepresentation[idx:idx+4])

			asciiRepresentation.append(chr(self.dnaEncodings[groupedProteins]))



		# Writing the ascii representation to the out directory
		if not self.outputDir:
			makedirs("out",exist_ok=True)
			self.outputDir="out"
		
		elif not path.exists(self.outputDir):
			makedirs(self.outputDir)

		fhandle=open(self.outputDir+"/"+'plaintext','w')
		
		for char in asciiRepresentation:
			fhandle.write(char)


	def kdge_encrypt(self):
		'''
			This function performs the encryption process and returns the ciphertext
		'''


		# List of bits of the keyfile
		keyFileBitsList = list()



		# Check for the keyfile existance
		if not self.keyFile:

			fh = open("key.k",'wb')

			for i in range(0,3):
				fh.write((randint(48,58)).to_bytes(1, 'little'))

			fh.close()

			self.keyFile="key.k"

			# Creat the keyfile first
			pass


		# Reading the keyfile
		fhandle = open(self.keyFile,'rb')
		keyBytes = fhandle.read(100)
		fhandle.close()



		for byte in keyBytes:
			keyFileBitsList += list(bin(byte)[2:].zfill(8))







		# Reading the plaintext file
		fhandle=open(self.plaintextFile,'r')
		lines = fhandle.readlines()
		fhandle.close()


		# Character encoding of the file
		plaintextFileCharEncoding = list()

		print(self.dnaEncodings)
		# Reading the characters of the plaintext file and encode them with dna-encodings and 
		# convert them to binary values using binary encoding.
		for line in lines:
			for char in line:
				dnaEncoding = self.dnaEncodings[ord(char)]
				print(dnaEncoding)
				plaintextFileCharEncoding+= list("".join([ self.dnaProEncodings[prot] for prot in dnaEncoding]))





		# XORing plaintext with the key

		# First, make key and the plaintext equal length
		differenceMul = len(plaintextFileCharEncoding) // len(keyFileBitsList)
		differenceMod = len(plaintextFileCharEncoding) % len(keyFileBitsList)
		newKey = keyFileBitsList*differenceMul + keyFileBitsList[:differenceMod]


	
		ciphertext = []


		for i in range(len(plaintextFileCharEncoding)):
			
			if ( plaintextFileCharEncoding[i]=='1' and newKey[i]=='1') or (plaintextFileCharEncoding[i]=='0' and newKey[i]=='0'):
				ciphertext.append('0')
			
			else:
				ciphertext.append('1')

	
		
		# Writing the ciphertext to the output directory, first check for existence
		# of the output directory, and create one if necessary
		if not self.outputDir:
			makedirs("out",exist_ok=True)
			self.outputDir="out"
		
		elif not path.exists(self.outputDir):
			makedirs(self.outputDir)

		fhandle=open(self.outputDir+"/"+'ciphertext','wb')
		
		for idx in range(0,len(ciphertext),8):
			fhandle.write(int("".join(ciphertext[idx:idx+8]),2).to_bytes(1, 'little'))


		# Dumping encodings

		with open(self.outputDir+"/"+"alphabet.enc", "wb") as fh:
			dump(self.dnaEncodings, fh)

		with open(self.outputDir+"/"+"dnaprot.enc", "wb") as fh:
			dump(self.dnaProEncodings, fh)


	

obj=Kdge()
obj.create_dna_alphabet_encoding()
obj.create_dna_protein_binaries()
obj.parse_command_arguments()




