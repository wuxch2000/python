
max = int(input("input max number:"))
a, b = 0, 1
while b <= max:
    print(b, end=' ', flush=True)
    a, b = b, a+b
print()

