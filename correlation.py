from re import X
import numpy as np

x = [1,2,3,4,5,6,7]
y = [21,31,41,51,13,42,67]
meanx = ((sum(x))/ (len(x)))
# print(meanx)
meany = ((sum(y))/ (len(y)))
# NUMERATOR
erxbar = list(map(lambda a: (a - meanx), x))
erybar = list(map(lambda a: (a - meany), y))
upper = [num*aw for num,aw in zip(erxbar,erybar)]
sumupper = sum(upper)
# DENOMINATOR
downx = list(map(lambda s: s**2, erxbar))
downx = sum(downx)
downy = list(map(lambda s: s**2, erybar))
downy = sum(downy)
down = ((downx * downy) ** 0.5)

r = sumupper / down
print(r)
r2 = np.corrcoef(x,y)[0,1]
print(r2)