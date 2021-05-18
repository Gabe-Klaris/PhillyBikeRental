test = [0,0]
for i in range(1,100):
    test.insert(1, i)
    test.pop(2)
    print(test)
    test.insert(0,i)
    test.pop(1)
