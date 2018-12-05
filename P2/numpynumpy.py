from numpy import load

data = load('Q1.npz')
lst = data.files
for item in lst:
    print(item)
    print(data[item])