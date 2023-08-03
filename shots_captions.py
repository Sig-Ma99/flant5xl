def para_caption1():
    combo = list()
    for i in [1, 2, 4, 8]:
        a = list()
        a.append(i)
        a.append(1)
        combo.append(a)
    return combo

def para_caption2():
    combo = list()
    for i in range(4):
        a = list()
        a.append(i)
        a.append(5)
        combo.append(a)
    for i in range(1,6):
        a = list()
        a.append(i)
        a.append(3)
        combo.append(a)
    for i in range(1,11):
        a = list()
        a.append(i)
        a.append(1)
        combo.append(a)
    return combo


print(para1())
print(para12())