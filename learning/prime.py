

def prime_number(n):
    count=0
    for i in range(1,n):
        is_prime = 1
        for j in range(2,i):
            if i%j == 0:
                is_prime = 0
                break
        if is_prime:
            count += 1
            print(i, end=',', flush=True)
    return count

max = int(input("input max number:"))
print("Prime number in range from 1 to", max)
c=prime_number(max)
print("\nTotal=",c)
