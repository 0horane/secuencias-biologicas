from copy import deepcopy

def combinaciones_k(secuencia: str, k: int):
    res = []
    for i in range(len(secuencia) - k + 1):
        res.append(secuencia[i:i+k])
    res.sort()
    return res

def combinaciones_de_pares(secuencia: str, k: int, d: int):
    res = []
    for i in range(len(secuencia) - (2*k + d) + 1):
        res.append((secuencia[i:i+k], secuencia[i + k + d:i + k + d + k]))
    res.sort()
    return res


def stringFromPath(k_mers):
    res = k_mers[0]
    for k_mer in k_mers[1:]:
        res += k_mer[-1]
    return res

def stringFromPathPares(kdMeros: list[tuple[str,str]], k:int, d:int):
    primerasComponentes = [x[0] for x in kdMeros]
    segundasComponentes = [x[1] for x in kdMeros]

    stringPrimerasComponentes = stringFromPath(primerasComponentes)
    stringSegundasComponentes = stringFromPath(segundasComponentes)

    print(stringPrimerasComponentes[k + d:], "PRIMERA")
    print(stringSegundasComponentes[:-(k + d)], "Segunda")
    if((stringPrimerasComponentes[k + d:] == stringSegundasComponentes[:-(k + d)])):
        return stringPrimerasComponentes+stringSegundasComponentes[-(k+d):]
    return "There is no string spelled by the gaped pattern."

class graph:
    def __init__(self, adyacencias, k_mers):
        
        self.adyacencias = adyacencias
        self.k_mers = k_mers

    

    @classmethod
    def from_overlap(cls, k_mers):
        graph = []
        for i, k_mer1 in enumerate(k_mers):
            adyacencias = list()
            graph.append(adyacencias)
            for j, k_mer2 in enumerate(k_mers):
                if k_mer1[1:] == k_mer2[:-1]:
                    adyacencias.append(j)
        return cls(graph, k_mers)

    @classmethod
    def debrujin_from_text(cls, k, text):
        k_mers = set()
        for i in range(len(text) - k + 2):
            k_mers.add(text[i:i+k-1])
        k_mers = list(k_mers)
        print(k_mers)
        adyacencias = [[] for i in range(len(k_mers))]
        for i in range(len(text) - k + 1):
            solapamiento1 = text[i:i+k-1]
            solapamiento2 = text[i+1:i+k]
            adyacencias[k_mers.index(solapamiento1)].append(k_mers.index(solapamiento2))
        return cls(adyacencias, k_mers)
        


    def eulerian_cycle(self):
        ciclo = [0]
        aristas = deepcopy(self.adyacencias)
        nodo = 0
        nodo = aristas[nodo].pop(0)
        while nodo != 0:
            ciclo.append(nodo)
            nodo = aristas[nodo].pop(0)
        ciclo.append(0)

        while sum([len(i) for i in aristas]) != 0:
            i = 0
            while len(aristas[ciclo[i]]) == 0:
                i += 1

            nodo_original = ciclo[i]
            ciclonuevo = [nodo_original]
            nodo = nodo_original
            nodo = aristas[nodo].pop(0)
            while nodo != nodo_original:
                ciclonuevo.append(nodo)
                nodo = aristas[nodo].pop(0)

            ciclo[ciclo.index(nodo_original):ciclo.index(nodo_original)] = ciclonuevo

        return ciclo

        
            
            
        


    def print_overlap(self):
        for i, k_mer1 in enumerate(self.k_mers):
            print(k_mer1, "->", ",".join([self.k_mers[j] for j in self.adyacencias[i] ]))

example_string = "TAATGCCATGGGATGTT"
example_list = [example_string[i:i+3] for i in range(len(example_string)-2)]
example_list212 = [(example_string[i:i+2],example_string[i + 3:i+5]) for i in range(len(example_string)-4)]


def testmain():
    #secuencia = input("input txt\n")
    #k = int(input("input len\n"))
    #print(combinaciones_k(secuencia, k))
    print(example_string)
    print(example_list)
    print(stringFromPath(example_list))
    print("")
    k_mers = combinaciones_k(example_string,3)
    #graph.from_overlap(k_mers).print_overlap()
    graph.debrujin_from_text(3,example_string).print_overlap()

    test_eulerian = [
        [2,3],
        [0,4],
        [3],
        [0,5],
        [5],
        [1,6],
        [1],
    ]
    test_eulerian_names = list(map(str,range(7)))

    a = graph(test_eulerian, test_eulerian_names)
    print(a.eulerian_cycle())

    print("\n\n\n\n\n\n", combinaciones_de_pares(example_string, 3, 1))
    print(example_list212)
    print(example_string)
    print(stringFromPathPares(example_list212,2,1))

def carsonellaRuddiiMain():
    with open("CarsonellaRuddii.txt") as genome:
        k_mers = genome.read().splitlines()
    graph.from_overlap(k_mers)
    



if __name__ == "__main__":
    #testmain()

    carsonellaRuddiiMain()

