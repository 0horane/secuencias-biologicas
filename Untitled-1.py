from itertools import islice
import numpy as np

def south_or_east(i,j,derecha,abajo):
    if i == j == 0:
        return 0
    x = -float('inf')
    y = -float('inf')
    if i > 0:
        x = south_or_east(i-1, j, derecha, abajo) + derecha[j][i - 1]
    if j > 0:
        y = south_or_east(i, j-1, derecha, abajo) + abajo[j - 1][i]
        
    return max(x,y)

"""
def south_or_east_dyn(n,m,derecha,abajo):
    cache = np.zeros((n+1,m+1))
    for i in range(1,n+1):
        cache[0][i]=cache[0][i-1]+abajo[0][i-1]
    for j in range(1,m+1):
        cache[j][0]=cache[j-1][0]+derecha[j-1][0]
    for i in range(1,n+1):
        for j in range(1,m+1):
            cache[j][i]=max( cache[j][i-1]+abajo[j][i - 1] ,cache[j-1][i]+derecha[j - 1][i] )

    print(cache)
    return cache[-1][-1]
"""
def south_or_east_dyn(n,m,derecha,abajo):
    cache = np.zeros((n+1,m+1))
    for i in range(1,n+1):
        cache[i][0]=cache[i-1][0]+abajo[i-1][0]
    for j in range(1,m+1):
        cache[0][j]=cache[0][j-1]+derecha[0][j-1]
    for i in range(1,n+1):
        for j in range(1,m+1):
            cache[i][j]=max( cache[i-1][j]+abajo[i - 1][j] ,cache[i][j-1]+derecha[i][j-1])
    print(cache)
    return cache[-1][-1]


def longest_common_subsequence(str1, str2):
    if str1 == '' or str2 == '':
        return 0

    valor_diagonal = int(str1[0] == str2[0])
    
    return max(
        longest_common_subsequence(str1[1:], str2[1:]) + valor_diagonal, 
        longest_common_subsequence(str1[1:], str2), 
        longest_common_subsequence(str1, str2[1:]))
"""
def longest_common_subsequence2(str1, str2):
    next1 = next(str1, None)
    next2 = next(str2, None)
    if next1 == None or next2 == None:
        return 0

    valor_diagonal = int(next1 == next2)
    
    return max(
        longest_common_subsequence2(str1[1:], str2[1:]) + valor_diagonal, 
        longest_common_subsequence2(str1[1:], str2), 
        longest_common_subsequence2(str1, str2[1:]))
"""

def longest_common_subsequence3(str1, str2, i, j):
    if str1 == '' or str2 == '':
        return 0

    valor_diagonal = int(str1[0] == str2[0])
    
    return max(
        longest_common_subsequence(str1[1:], str2[1:]) + valor_diagonal, 
        longest_common_subsequence(str1[1:], str2), 
        longest_common_subsequence(str1, str2[1:]))


def main():
    with open("Derecha.txt") as derechaFile:
        derecha = [[int(y) for y in x.split(",")] for x in derechaFile.read().splitlines()]
    with open("Abajo.txt") as abajoFile:
        abajo = [[int(y) for y in x.split(",")] for x in abajoFile.read().splitlines()]
    print(np.array(derecha))
    print(np.array(abajo))
    print(south_or_east(4,4,derecha,abajo))

    #print(longest_common_subsequence('GCCCAGTCTATGTCAGGGGGCACGAGCATGCACA', 'GCCGCCGTCGTTTTCAGCAGTTATGTTCAGAT'))
    #print(longest_common_subsequence3(list('GCCCAGTCTATGTCAGGGGGCACGAGCATGCACA'), list('GCCGCCGTCGTTTTCAGCAGTTATGTTCAGAT')))
    #print(longest_common_subsequence2(islice('GCCCAGTCTATGTCAGGGGGCACGAGCATGCACA',None), islice('GCCGCCGTCGTTTTCAGCAGTTATGTTCAGAT',None)))
    
    print("res",south_or_east_dyn(4,4,derecha,abajo))

if __name__ == "__main__":
    main()