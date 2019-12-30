#! /usr/bin/python3

import sys
import random

class Stack():
	def __init__(self):
		self.stack = []

	def pop(self):
		return self.stack.pop() if self.stack else 0

	def push(self, nums):
		if type(nums) is list:
			for num in nums: self.stack.append(num)
		else: self.stack.append(nums)


class Backhand_Interpreter():
	def __init__(self, code):
		self.main  = Stack()
		self.other = Stack()

		self.pointer = 0
		self.code = code
		self.quote = False
		self.dir = 1
		self.step = 3
		self.excessChar = None
		self.debug = False
		self.register = None

	def outputOne(self):
		o = self.pop()
		if o > -1: sys.stdout.write(chr(o))
		else: self.error("Tried to print negative value (%d) as character\n"%o)

	def outputAll(self):
		while self.main.stack: self.outputOne()
		
	def tick(self):i.changePointer(i.step*i.dir, False)

	def changePointer(self, num, evl = True):
		self.pointer += num
		check = True
		while check:
			check = False
			if self.pointer >= len(self.code):
				self.pointer = len(self.code) - (self.pointer - len(self.code)) - 2
				self.dir = -self.dir
				check = True
			elif self.pointer < 0:
				self.pointer = -self.pointer
				self.dir = -self.dir
				check = True
		if evl: self.pointer -= self.dir*self.step

	def push(self, nums): self.main.push(nums)
	def pop(self): return self.main.pop()

	def getChar(self):
		if self.excessChar:
			c = self.excessChar
			self.excessChar = None
		else:
			c = sys.stdin.read(1)
			c = ord(c) if c else -1
		return c

	def getNumber(self):
		x = 0
		while x != -1 and chr(x) not in '0123456789':
			y = x
			x = self.getChar()
		if x == -1: return -1
		n = int(chr(x))
		x = self.getChar()
		while x != -1 and chr(x) in '0123456789':
			n = n*10 + int(chr(x))
			x = self.getChar()
		self.excessChar = x
		if chr(y) == '-': n = -n
		return n

	def run(self):
		c = self.code[self.pointer]
		if self.debug:
			print(self.code)
			print(' '*self.pointer +'^')
			print(self.main.stack)
			print(self.other.stack)
			input()
		if self.quote:
			if c == '"': self.quote = False
			else: self.main.push(ord(c))
			
		# Literals
		elif c in '0123456789abcdef': self.push('0123456789abcdef'.index(c))
		elif c == '"': self.quote = True
		elif c == "'":
			self.tick()
			self.push(ord(self.code[self.pointer]))
		
		# Stack manipulation
		elif c == '~': self.pop()
		elif c == '$': self.push([self.pop(), self.pop()])
		elif c == ':': self.push([self.pop()]*2)
		elif c == '&':
			if self.register != None:
				self.push(self.register)
				self.register = None
			else:
				self.register = self.pop()
		elif c == 'r': self.main.stack = self.main.stack[::-1]
		elif c == 'l': self.push(len(self.main.stack))
		elif c == '(': self.push(self.other.pop())
		elif c == ')': self.other.push(self.pop())
		elif c == 'x': self.main, self.other = self.other, self.main
		
		# Control Flow
		elif c == '<': self.dir = -1
		elif c == '>': self.dir = 1
		elif c == '{': self.changePointer(-1)
		elif c == '}': self.changePointer(1)
		elif c == '^': self.step += 1
		elif c == 'M': self.step += 2
		elif c == 'v': self.step -= 1
		elif c == 'W': self.step -= 2
		elif c == '?': self.changePointer(random.choice([-1,1]))
		elif c == 'j':
			self.pointer = 0
			self.dir = 1
			self.changePointer(self.pop())
		elif c == 's': 
			self.changePointer(self.pop()*self.dir)
		elif c == '@': return False
		
		# Branching
		elif c == '_': self.changePointer(-1 if self.pop() else 1)
		elif c == '|': self.dir = -self.dir if self.pop() else self.dir
		elif c == '!': self.push(int(not self.pop()))
		elif c == 'L': self.push(int(self.pop() < self.pop()))
		elif c == 'G': self.push(int(self.pop() > self.pop()))
		elif c == 'E': self.push(int(self.pop() == self.pop()))
		
		# Arithmetic
		elif c in '*/%+-':
			a,b = self.pop(), self.pop()
			if c == '/': 
				c = '//'
				if a == 0: self.error("Attempted to divide by zero")
			self.push(eval(str(b)+c+str(a)))
		elif c == '[': self.push(self.pop()-1)
		elif c == ']': self.push(self.pop()+1)
		
		# IO
		elif c == 'i': self.push(self.getChar())
		elif c == 'o': self.outputOne()
		elif c == 'I': self.push(self.getNumber())
		elif c == 'O': sys.stdout.write(str(self.pop()))
		elif c == '\n':print()
		elif c == 'H': return self.outputAll() and False
		elif c == 'h': return sys.stdout.write(str(self.pop())) and False

		return True

	def error(self, message): 
		sys.stderr.write(message + "\n")
		exit(1)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		program = open(sys.argv[1], "r").read()
		i = Backhand_Interpreter(program)
		if not program:
			i.error("Program cannot be empty")
		#i.debug = True
		while i.run(): i.tick()

