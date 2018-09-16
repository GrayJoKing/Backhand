

"""
0-f  Push number
<>   Change direction
{}   Shift left/right one and execute
()   Push/pull from other stack
x    Swap stacks
*+-/% Arithmetic operators
~    Pop
:    Dupe
$    Swap
!    Not
[]   Decrement/increment top of stack
r    Reverse stack
l    Push length of stack
\n   Print a newline
i/o  Input/Output as char code
I/O  Input/Output as number
"    Push values until next "
j    Jump to the nth instruction
@    End program
H    End program and output stack
^    Increase step
v    Decrease step
?    Step left or right randomly
_    Pop and if zero step right else step left
|    Pop and if not zero reverse direction
&    Pop and store/push from register
"""

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

	def stringify(self):
		return [chr(a)for a in self.stack[::-1]]

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
			c = ord(c) if c != '' else -1
		if c == -1: return -1
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
		elif c in '0123456789abcdef': self.push('0123456789abcdef'.index(c))
		elif c == '@': return False
		elif c == 'H': return 0*sys.stdout.write(''.join(self.main.stringify()))
		elif c == '"': self.quote = True
		elif c == '<': self.dir = -1
		elif c == '>': self.dir = 1
		elif c == '{': self.changePointer(-1)
		elif c == '}': self.changePointer(1)
		elif c == '[': self.push(self.pop()-1)
		elif c == ']': self.push(self.pop()+1)
		elif c == '(': self.push(self.other.pop())
		elif c == ')': self.other.push(self.pop())
		elif c == 'x': self.main, self.other = self.other, self.main
		elif c in '*/%+-':
			if c == '/': c = '//'
			a,b = str(self.pop()), str(self.pop())
			self.push(eval(b+c+a))
		elif c == '!': self.push(int(not self.pop()))
		elif c == '~': self.pop()
		elif c == ':': self.push([self.pop()]*2)
		elif c == '$': self.push([self.pop(), self.pop()])
		elif c == 'r': self.main.stack = self.main.stack[::-1]
		elif c == 'l': self.push(len(self.main.stack))
		elif c == '\n':print()
		elif c == 'i': self.push(self.getChar())
		elif c == 'o': sys.stdout.write(chr(self.pop()))
		elif c == 'I': self.push(self.getNumber())
		elif c == 'O': sys.stdout.write(str(self.pop()))
		elif c == 'j':
			self.pointer = 0
			self.dir = 1
			self.changePointer(self.pop())
		elif c == '^': self.step += 1
		elif c == 'v': self.step -= 1
		elif c == '?': self.changePointer(random.choice([-1,1]))
		elif c == '_': self.changePointer(-1 if self.pop() else 1)
		elif c == '|': self.dir = -self.dir if self.pop() else self.dir
		elif c == '&':
			if self.register != None:
				self.push(self.register)
				self.register = None
			else:
				self.register = self.pop()

		return True


if __name__ == "__main__":
	if len(sys.argv) > 1:
		program = open(sys.argv[1], "r").read()
		i = Backhand_Interpreter(program)
	else:
		i = Backhand_Interpreter('aO0{@|}}:\n.O[.')
		i.debug = True
	while i.run(): i.changePointer(i.step*i.dir, False)

"""
Examples:

Hello, World!:
"ol!,ld elWHro"

Add two numbers from stdin:
IO+I@

Cat Program:
io

Truth Machine:
I|@}:  O

Quine:
"  v < ^:3+fb+v}< [o:$}| @

Countdown from 10
aO0{@|}}:
 O[

Count up forever
]{O: 

Factorial
1@ IO :~!{|{}: ([ *)

"""
