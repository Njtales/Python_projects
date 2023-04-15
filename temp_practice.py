def fun(n):
    s = '+'
    for i in range(n):
        s += s
        yield s

for i in fun(3):
    print(i)