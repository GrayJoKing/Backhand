# Backhand

Backhand is an esoteric language with an unusual program flow, inspired by 2D languages, such as Befunge and `><>`.

Backhand is a 1D language, so most programs are interpreted as a series of characters. The origin of the name comes from "Back and Forth", since to get the most out of the code, the instruction pointer has to go back and forth. Initially, the pointer will start at the first character and move 3 steps at a time. For example: <code>1&nbsp;&nbsp;1&nbsp;&nbsp;+&nbsp;&nbsp;O&nbsp;&nbsp;@</code> will add 1 + 1 and output 2 before terminating.

If the pointer is about to step out of bounds, it reverses direction. Using this, `1O.1+@` is the same program as before. The program evaluation goes like so:

```
1  1     Bounce off end and go left
 O  +    Bounce off start and go right
  .  @   End
```

This can lead to some very compressed programs folding in on themselves, like `"ol!,ld elWHro"` printing `Hello, World!`.

But if you want to decrease the step count of the pointer, you can with `v`. The program `v v"!dlroW ,olleH"H` first changes the step count to 1 and then prints `Hello, World!`. If you want to go the other way, you can use `^` to increase the pointer steps. Note that if you decrease the step count to negative then directionals like `<>` will have the opposite effect.



## Data structure

Similar to [Brain-Flak](https://github.com/DJMcMayhem/Brain-Flak), Backhand uses two separate stacks. You usually operate on the main stack, but you can pull/push to the other stack with `(` or `)`, or even switch stacks with `x`. Attempting to pop from an empty stack yields a `0` instead.


## Operators

| Group | Character(s) | Name | Action |
|---|---|---|---|
| Literals |  |  |
|          | `0-9a-f` | Number | Pushs the appropriate number. The characters `a` to `f` push the values `10` to `15` |
|          | `"`      | String | Turn on string mode, which pushes the ASCII value of each character until it reaches either another `"` |
|          | `'`      | Character | Push the ordinal value of the next instruction instead of executing it |
| Stack manipulation |  |  |
|                    | `~` | Pop     | Pop and discard `a` |
|                    | `$` | Swap    | Pop `a` then `b` and push `a` then `b` |
|                    | `:` | Dupe    | Pop `a` then push `a` twice |
|                    | `&` | Register | If there is not a value in the register, pop `a` and store `a` in the register. Otherwise, push the value in the register and clear it |
|                    | `r` | Reverse | Reverse the stack |
|                    | `l` | Length  | Push the length of the stack |
|                    | `(` | Pull    | Pop `a` from the other stack and push `a` |
|                    | `)` | Push    | Pop `a` and push `a` to the other stack |
|                    | `x` | Switch  | Swap the main and other stack |
| Control Flow |  |  |
|              | `<` | Left  | Change direction to left |
|              | `>` | Right | Change direction to right |
|              | `{` | Step Left | Step left one |
|              | `}` | Step Right | Step right one |
|              | `^` | Increment Step | Increase the step value by 1 |
|              | `M` | Double Increment Step | Increase the step value by 2 |
|              | `v` | Decrement Step | Decrease the step value by 1 |
|              | `W` | Double Decrement Step | Decrease the step value by 2 |
|              | `?` | Random | Step left or right randomly |
|              | `j` | Jump | Pop `a` and jump to the `a`th character, bouncing off the sides as usual. `0` represents the first character |
|              | `s` | Skip | Pop `a` and skip forward `a` characters, bouncing off the sides as usual. This moves forward in the current direction |
|              | `@` | Terminate | End the program |
| Branching  |  |  |
|            | `_` | Decision Step    | Pop `a` and if `a` is zero step right, else step left |
|            | `\|` | Decision Change | Pop `a` and if `a` is not zero reverse direction |
|            | `!` | Not     | Pop `a` and push `1` if `a` is equal to `0`, otherwise `0` |
|            | `L` | Less    | Pop `a` then `b` and push `1` if `a` is less than `b`, otherwise `0` |
|            | `G` | Greater | Pop `a` then `b` and push `1` if `a` is greater than `b`, otherwise `0` |
|            | `E` | Equal   | Pop `a` then `b` and push `1` if `a` is equal to `b`, otherwise `0` |
| Arithmetic |  |  |
|            | `-` | Subtraction    | Pop two values `a` then `b` and push `b-a` |
|            | `+` | Addition       | Pop two values `a` then `b` and push `b-a` |
|            | `*` | Multiplication | Pop two values `a` then `b` and push `b*a` |
|            | `/` | Division       | Pop two values `a` then `b` and push `b//a`, the integer division of `b` and `a` |
|            | `%` | Modulo         | Pop two values `a` then `b` and push `b%a`, where the sign of the result matches the sign of `a` |
|            | `[` | Decrement      | Pop `a` and push `a-1` |
|            | `]` | Increment      | Pop `a` and push `a+1` |
| Input/Output |  |  |
|              | `i`  | ASCII input | Push the next byte of input |
|              | `o`  | ASCII output | Pop `a` and output `a` as ASCII |
|              | `I`  | Number input | Ignore input data until it reaches a number and push that number. If the number is preceeded by a `-` then the number is negative. |
|              | `O`  | Number output | Pop `a` and print `a` as a number |
|              | `\n` | Newline | Print a newline |
|              | `H`  | Halt | Print the contents of the stack as a string and terminate the program |
|              | `h`  | Finish | Output the top of stack as a number and terminate the program |

Any other character is ignored.

## Example programs:

### Countdown from 10
```
aO0{@|}}:
.O[.
```

### Hello, World!
`"ol!,ld elWHro"`

### Cat program
`io`

### Truth Machine
`I|@}:  O`

### Count up forever:
`]{O:.`

### Factorial:
`1@ IO :~!{|{}: ([ *).`

### Quine:
`"#v{<@^:[ba+0v|{$:o[}`

### Printing Backhand
`"acdBkn"haH`
