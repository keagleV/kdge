

from re import match



class KdgeEALogger:
	'''
		This class has implemented the logger functionality which is going
		to be used through the program
	'''

	def log_message(self,message,status,lineNumer=None):

		'''
			This function will log the message to the console
		'''

		print("[{0}]{1} {2} ".format(status,'' if lineNumer is None else ' L-'+str(lineNumer)+'  ' ,message))




class EAparams:
	'''
		This class has implemented the parameter configuration of the 
		EA algorithm
	'''

	def __init__(self):

		# Population size
		self.popSize= 10


		# Generation Count
		self.genCount=10

		# Crossover probability
		self.crossProb = 0.1


		# Mutation Probability
		self.mutProb = 0.9

		# Mutation Operation
		self.mutOp = "sbf"

		# Crossover Operation
		self.crossOp = "spc"

		# Crossover k-point crossover k value
		self.crossKValue = 2


		# Logger Handler
		self.logHandler = KdgeEALogger()


		'''
			Parameter definition regexes
		'''


		# Population size
		self.popSizer = '\s*POP_SIZE\s*=\s[1-9][0-9]*\s*'

		# Generation evolution count
		self.genNumr = '\s*GEN_NUM\s*=\s*[1-9][0-9]*\s*'

		# Crossover Prob
		self.crossProbr = '\s*CROSS_PROB\s*=\s((?!0+(?:\.0+)?$)\d?\d(?:\.\d\d*)?)\s*'

		# Mutation prob 
		self.mutProbr = '\s*MUT_PROB\s*=\s((?!0+(?:\.0+)?$)\d?\d(?:\.\d\d*)?)\s*'


		# Mutation operator
		# 1. sbf: single bit flap
		# 2. mbf: multi bit flap
		self.mutOpr= '\s*MUT_OP\s*=\s*(sbf|mbf)\s*'

		# Crossover operator
		# 1. spc: single point crossover
		# 2. kpc: k-point crossever
		self.crossOpr= '\s*CROSS_OP\s*=\s*(spc|2pc|rot)\s*'



		self.logMessages = {
			'PARAMETER_DEFINITION_ERR' : 'Parameter Definition Error',
		}

	
	def read_params(self,file):
		'''
			This function will read the parameters from the file
		'''

		fhandle=open(file)

		lines=fhandle.readlines()

		fhandle.close()


		for lineNum,line in enumerate(lines):

			line=line.strip()

			if line:

				if line.startswith('#'):
					continue

				if match(self.genNumr,line):
					self.genCount= int (line.split("=")[1].strip())

				elif match(self.popSizer,line):
					self.popSize= int (line.split("=")[1].strip())

				elif match(self.mutProbr,line):
					self.mutProb= float (line.split("=")[1].strip())

				elif match(self.crossProbr,line):
					self.crossProb = float (line.split("=")[1].strip())

				elif match(self.mutOpr,line):
					self.mutOp = str (line.split("=")[1].strip())

				elif match(self.crossOpr,line):
					self.crossOp = str (line.split("=")[1].strip())


				else:
					self.logHandler.log_message(self.logMessages['PARAMETER_DEFINITION_ERR'],'ERR',lineNum+1)
					exit(1)