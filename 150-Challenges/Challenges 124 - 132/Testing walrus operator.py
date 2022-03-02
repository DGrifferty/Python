import random

num = 6
div = 5

if (n := num % div) != 0:
    print(f'number {num} divided by {div} has a remainder of {n}')

for i in range(101):
    if i % 2 == 0 and i != 0:
        print(f'{i} is even')
    elif i !=0:
        print(f'{i} is odd')
print("fin -  creating a random list")

# Creating list

lst1 = []
for i in range(100):
    lst1.append(random.randint(0, 80000))

lst1.sort()
print(lst1)
for i in lst1:
    if i % 2 == 0 and i != 0:
        print(f'{i} is even')
    elif i != 0:
        print(f'{i} is odd')
