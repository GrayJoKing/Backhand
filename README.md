# Backhand

Backhand is an esotoric language with an unusual program flow, where instructions will be evaluated left to right, but only executed right to left. For example, take the short program:

`n5+n1`

`n` is the print number instruction, returning that number afterwards. This program prints the `1` first, before adding it to the 5 and printing a `6`. This becomes more obvious with something like:

`n5+4-3*2/1`

Where the operaters are executed from right to left, printing `3`.

## Data types
There is only one data type in Backhand, lists of number. However, a list with only one element is often treated as a single integer, and most operators will act on the last element of the list. Sometimes it's easier to think of it as a stack.

## Behaviour
Many operators will behave differently whether or not there is data to the left of it. For example, the `!` operator will return the factorial of the left data, but will return the boolean NOT of the right if there is no data. If an operator doesn't have a function for that situation it will just return the value of itself.

## Variables
Variables names can be any numeric value. For example `a` returns `97`, so `a=31` will set `a` to `31`. However, calling `a` from now on will return the value `31`, so `a=97` will not restore `a`, but sets `37` to `97`. You'll need the `*` operator to make sure you're actually fetching the original value of `a`, where `*a=97` is the correct version of this. 

**Warning: you can set operators to values.** For example, `*5=1` will set the value of `5` to `1`, meaning something like `1+5` will now return `2` instead of `6`. Even worse, you can reassign the `=` operator itself, e.g. `*==0`, which really ruins your day. Any operators set in this manner will be lost *forever*, so be careful!

## Operators

| Character | Use |  With left | With right |
|---|---|---|---|
| `0-9` | Number literals | If number mode is active, it multiplies the previous value by 10 and adds itself to it. Otherwise it just appends itself to the list. Either way, it activates number mode and continues right. Number mode is deactivated when a non-number is reached. | Ditto |
| `-` | Subtraction/Negation | Return left - right | Return -right |
| `+` | Addition | Return left + right | Push "+" to left |
| `/` | Division | Return left / right (integer division) | Push "/" to left |
| `%` | Modulo | Return left % right | Push "%" to left |
| `*` | Multiplication/Fetch | Return left * right | Push the ASCII value of the next character to left. EOF is treated as 0. |
| `=` | Set | Set the data at left to right |  Push "=" to left |
| `"` | String | Push the ASCII value of each character until it reaches either another `"` or EOF | Ditto |
| `i` | ASCII input | Push the next byte of input | Ditto |
| `o` | ASCII output | Print left as ASCII | Print right as ASCII |
| `n` | Number input | Ignore data until it reaches a `-`, `+` or a number and push that number | Ditto |
| `b` | Number output | Print left as space separated numbers | Print right as space separated numbers |
| `<` | Evaluate without pushing | Evaluate right without affecting left | Ditto |
| `(` | Evaluate | Push right with a new instance of left | Ditte |
| `?` | If | If left is non-zero, continue. Otherwise skip to the next `:`. | If right is non-zero, continue. Otherwise skip to the next `:` |
| `{` | Do while | Execute the right code until it returns 0. Return a list of the values returned by each loop | Ditto |
| `:;)}>`, EOF | End Evaluation | Return left | Push 0 and return |
| whitespace | Ignored | Ignored. Used to break up numbers. | Ditto |


## Example programs:

### Countdown from 10
`a=11;n{*a=a-1`

### Hello, World!
`o"Hello, World!`

### Cat program
`o{i` for non-infinite streams
`{oi` for infinite

### Count up forever:
`{n*0=0+!!o5+5`

### Factorial:
`nb!`

### Quine:
`a=";o*a61 34a34a";o*a(=34a34a`

