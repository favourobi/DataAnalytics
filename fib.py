i, j = 0, 1 #python swapping.
k=[]
k.append(i)
while i < 100:
    #print(i)
    i, j = j, i + j #Swap again
    k.append(i)

del(k[len(k)-1])
print(k)
#for t in k:
 #   print(t)