import sys
import math

##0-9 (aliases for actual numbers)
#If left argument:
	#eval right(left*10 + self)
#Else
	#Return 0-9

#A-Z and a-z
#If left argument:
	# return eval(left.append(self))
#Else
	#Return eval(self)

##= (set)
#If left argument:
	#Set left variable to eval(right)
	#return right
#Else:
	#Return self

##/+-% (arithemetic)
#If left argument
	#Return left arithmetic eval(right)
#Else
	#Return self

##* (multiply or pointer)
#If left argument
	#Return left*eval(right)
#else
	#return next character

##! (not)
#If left:
	#return factorial(left)
#else:
	#return not eval(right)

##;
#If left argument
	#Return left argument
#Else
	#Return self

##i (input)
#If input:
	#Return a byte of input
#else:
	##return 0

##o (output)
#if left argument:
	#return value of o
#else
	#Evaluate right and output it
	#Return right

##? (if statement)
#If left argument:
	#If left != 0
		#return eval right
	#else
		#eval right without executing anything and return 0
#else
	#if eval right:
		#return eval right
	#else:
		#eval right without executing anything and return 0

##r (random)
#if left:
	#return random number between left and right()
#else:
	#return a random element of the right() list

# space tab newline (no-ops)
##ignore them unless an * is in front

#{ (while loop)
#if left:
	#repeat loop while left variable is true
#else:
	#skip back to here if right() is true

#< (eval and return 0)
#right() and right(left)

#( (eval)
#return right()


class Backhand_Interpreter():
	def __init__(self, code, inp = '', inputFlag = 'preset', debug=False, step=False):
		self.debug = debug
		self.step = step

		self.inputFlag = inputFlag

		self.inp = list(inp[::-1])

		self.code = list(code)
		self.IP = -1
		self.intMode = -2

		self.constants = {}
		#Declare number constants 0-9
		for i in range(ord('0'), ord('9')+1):
			self.constants[i] = {
				'function'	: self.number,
				'value'		: i-ord('0')
			}

		#Arithemetic
		self.constants[ord("/")] = {
			'function'	: self.divide,
			'value'		: ord("/")
		}
		self.constants[ord("+")] = {
			'function'	: self.add,
			'value'		: ord("+")
		}
		self.constants[ord("-")] = {
			'function'	: self.subtract,
			'value'		: ord("-")
		}
		self.constants[ord("%")] = {
			'function'	: self.modulo,
			'value'		: ord("%")
		}
		self.constants[ord("*")] = {
			'function'	: self.multiply,
			'value'		: ord("*")
		}
		self.constants[ord("!")] = {
			'function'	: self.notFact,
			'value'		: ord("!")
		}

		#Variables
		self.constants[ord("=")] = {
			'function'	: lambda left, value: self.character(left, value) if not left else self.set(left,self.evaluate()),
			'value'		: ord("=")
		}
		self.constants[ord('"')] = {
			'function'	: self.string,
			'value'		: ord('"')
		}

		#IO
		self.constants[ord("i")] = {
			'function'	: lambda left, value: self.character(left, self.asciiIn()),
			'value'		: ord("i")
		}
		self.constants[ord("o")] = {
			'function'	: lambda left, value: self.evaluate(self.asciiOut(left)) if left else self.asciiOut(self.evaluate()),
			'value'		: ord("o")
		}
		self.constants[ord("n")] = {
			'function'	: lambda left, value: self.evaluate(self.intOut(left)) if left else self.intOut(self.evaluate()),
			'value'		: ord("n")
		}
		self.constants[ord("b")] = {
			'function'	: lambda left, value: self.number(left, self.intIn()),
			'value'		: ord("m")
		}

		#No-ops
		for x in " \t\n\r":
			self.constants[ord(x)] = {
				'function'	: self.evaluate,
				'value'		: ord(x)
			}

		#Control flow
		self.constants[ord("<")] = {
			'function'	: self.ignore,
			'value'		: ord("<")
		}
		self.constants[ord("(")] = {
			'function'	: self.brack,
			'value'		: ord("(")
		}
		self.constants[ord("?")] = {
			'function'	: lambda left, value: self.evaluate() if bool(self.evaluate() if not left else left) else self.skip(),
			'value'		: ord("?")
		}
		self.constants[ord("{")] = {
			'function'	: self.loop,
			'value'		: ord("{")
		}

		#End execution
		for x in ";)}>:":
			self.constants[ord(x)] = {
				'function'	: lambda left, value: left if left else [0],
				'value'		: ord(x)
			}

		while self.IP < len(code):
			self.evaluate()

	#Arithemetic
	def add(self, left, value):
		if left:
			temp = self.evaluate()
			left.append(left.pop() + temp.pop())
			return left
		else:
			return self.character(left, value)

	def divide(self, left, value):
		if left:
			temp = self.evaluate()
			if temp[0] == 0: raise("Error: Division by 0")
			left.append(left.pop()//temp.pop())
			return left
		else:
			return self.character(left, value)

	def subtract(self, left, value):
		if left:
			temp = self.evaluate()
			left.append(left.pop()-temp.pop())
			return left
		else:
			temp = self.evaluate()
			left.append(-left.pop())
			return left

	def modulo(self, left, value):
		if left:
			temp = self.evaluate()
			if temp[0] == 0: raise("Error: Modulo by 0")
			left.append(left.pop()%temp.pop())
			return left
		else:
			return self.character(left, value)

	def multiply(self, left, value):
		if left:
			temp = self.evaluate()
			left.append(left.pop()*temp.pop())
			return left
		else:
			return self.evaluate(self.character(left, self.get()))

	def notFact(self, left, value):
		if left:
			left.append(math.factorial(left.pop()))
			return self.evaluate(left)
		else:
			return [int(not self.evaluate().pop())]


	def ignore(self, left, value):
		self.evaluate()
		return self.evaluate(left)

	def brack(self, left, value):
		return self.character(left, self.evaluate())

	def evaluate(self, left=None, value=None):
		if left == None: left = []
		if self.step: input()
		self.IP += 1
		if self.IP >= len(self.code): return left if left else [0]
		return self.execute(ord(self.code[self.IP]), left)

	def execute(self, value, left):
		if self.debug: sys.stderr.write("Character: " + chr(value) + " Left: " + str(left) + "\n")
		if value in self.constants:
			return self.constants[value]['function'](left, self.constants[value]['value'])
		else:
			return self.character(left, value)

	def skip(self):
		if self.debug: sys.stderr.write('Skipping from ' + str(self.IP) + ' to ')
		while self.IP < len(self.code) and self.code[self.IP] != ":": self.IP += 1
		if self.debug: sys.stderr.write(str(self.IP) + "\n")
		return self.evaluate(0)

	def number(self, left=0, n=0):
		if left == None: left = 0
		num = 0
		if self.intMode == self.IP-1: left.append(left.pop()*10+n)
		else: left.append(n)
		self.intMode = self.IP
		return self.evaluate(left)

	def character(self, left = None, char = 0):
		if self.debug: sys.stderr.write('Pushing character ' + str(char) + "\n")
		if left == None: left = []
		if type(left) is not list: left = [left]
		if type(char) is not list: left.append(char)
		else: left = left + char
		return self.evaluate(left)

	def set(self, left, value):
		if type(left) is not list: left = [left]
		for n in left:
			if self.debug: sys.stderr.write('Setting ' + str(left) + ' to ' + str(value) + "\n")
			self.constants[n] = {
				'function'	: self.number if type(value) == int else self.character,
				'value'		: value
			}
		return value

	def get(self):
		self.IP += 1
		if self.IP >= len(self.code):
			return 0
		else:
			return ord(self.code[self.IP])

	def string(self, left, value):
		if not left: left = []
		if type(left) is not list: left = [left]
		temp = self.get()
		while temp and temp != value:
			left.append(temp)
			temp = self.get()
		if self.debug: sys.stderr.write('Pushed string ' + str(left) + "\n")
		return self.evaluate(left)

	def loop(self, left, value):
		if not left: left = []
		if type(left) is not list: left = [left]
		here = self.IP
		temp = self.evaluate()
		if self.debug: sys.stderr.write("Loop value " + str(temp) + "\n")
		while temp and (type(temp) != list or len(temp) != 1 or temp[0]):
			left += temp
			self.IP = here
			temp = self.evaluate()
			if self.debug: sys.stderr.write("Loop value " + str(temp) + "\n")
		if self.debug: sys.stderr.write("Loop ended and returned" + str(left) + "\n")
		return left

	def asciiIn(self):
		if self.debug: sys.stderr.write('Getting input character' + "\n")
		if self.inputFlag == 'preset':
			return ord(self.inp.pop()) if self.inp else 0
		else:
			return sys.stdin.read(1)

	def asciiOut(self, value):
		if type(value) is not list: value = [value]
		value = list(map(chr, value))
		if self.debug: sys.stderr.write('Printing ASCII ' + ''.join(value) + "\n")
		sys.stdout.write(''.join(value))
		return value

	def intOut(self, value):
		if self.debug: sys.stderr.write('Printing number ' + str(value) + "\n")
		sys.stdout.write(' '.join(map(str, value)))
		return value

	def intIn(self):
		if self.debug: sys.stderr.write('Getting input number' + "\n")
		temp = chr(self.asciiIn())
		while temp and temp not in "-+0123456789":
			temp = chr(self.asciiIn())
		if temp == 0: return 0
		num = 0
		sign = 1
		if temp == "-": sign = -1
		elif temp != "+": num = int(temp)

		temp = chr(self.asciiIn())
		while temp and temp in "0123456789":
			num = num*10 + int(temp)
			temp = chr(self.asciiIn())
		return num*sign



if __name__ == "__main__":
	program = open(__import__("sys").argv[1], "r").read()
	Backhand_Interpreter(program)

"""
debugMode = 0

Backhand_Interpreter('{n*0=0+!<o5+5',inp='',debug=debugMode,step=debugMode)
"""
"""
Countdown from 10
a=11;n{*a=a-1

Hello, World!
o"Hello, World!

Cat program
o{i

Count up forever:
{n*0=0+!!o*\n

Factorial:
nb!

Quine:
a=";o*a61 34a34a";o*a(=34a34a

"""

###Bugs
#What if self.number recieves a list? nb(oi
