# Part 1:

# 1) my_str.split() turns the string into a list of words (split by whitespace).
# 2) first = 1 means start from the 2nd word (index 1).
# 3) third = 2 means jump by 2 each time -> indices 1, 3, 5, ...
# 4) The while-loop appends those words into res.
# Result: res contains every other word starting from the second word.

my_str = "The first one is the easiest!"
res_oneliner = my_str.split()[1::2]


# Part 2:

# 1) Loops x = 100, 97, 94, ..., 1 (step -3).
# 2) For each x:
#    - if x % n == 0: store "x is divided by n.\n"
#    - else: store "the remainder of x divided by n is: (x % n).\n"
# 3) Prints all values in order, with sep="" so outputs are concatenated.

n = 42
print(*(f"{x} is divided by {n}.\n" if x % n == 0 else f"the remainder of {x} divided by {n} is: {x % n}.\n"
        for x in range(100, 0, -3)), sep="")


# Part 3:

# 1) Loops over i from 0 up to max(ord('9'), ord('z'), ord('Z')) inclusive.
# 2) Converts i -> character with chr(i).
# 3) Prints only if the character is a letter or a digit.
# Result: prints lines for '0'-'9', 'A'-'Z', and 'a'-'z'.

print(*(f"The ASCII number {i} represent the char '{chr(i)}'"
        for i in range(0, max(ord('9'), ord('z'), ord('Z')) + 1)
        if chr(i).isalpha() or chr(i).isdigit()),
      sep="\n")


# Part 4:

# 1) Starts an empty string.
# 2) For each number in list_c, converts it to a character using chr(num).
# 3) Appends to the string, then prints it at the end.
# Result: prints the decoded text represented by the ASCII codes.

list_c = [80, 121, 116, 104, 111, 110, 32, 105, 115, 32, 102, 117, 110, 33]
print("".join(map(chr, list_c)))