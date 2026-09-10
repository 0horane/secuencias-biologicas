from copy import deepcopy
import numpy as np
from math import factorial
from collections import defaultdict, Counter

# Separa string en kmeros de longitud K
def combinaciones_k(secuencia: str, k: int):
    res = []
    for i in range(len(secuencia) - k + 1):
        res.append(secuencia[i:i+k])
    res.sort()
    return res


# Separa string en pares de kmeros de longitud K separados por una distancia d
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

    #print(stringPrimerasComponentes[k + d:], "PRIMERA")
    #print(stringSegundasComponentes[:-(k + d)], "Segunda")
    if((stringPrimerasComponentes[k + d:] == stringSegundasComponentes[:-(k + d)])):
        return stringPrimerasComponentes+stringSegundasComponentes[-(k+d):]
    return "There is no string spelled by the gaped pattern."

class graph:
    def __init__(self, adyacencias, k_mers):
        
        self.adyacencias : list[list[int]] = adyacencias
        self.k_mers : list[str] = k_mers
        
    # toma lista de kmeros, genera grafo de ahi
    @classmethod
    def from_overlap(cls, k_mers, debug=False):
        distinct_kmers = list(set(k_mers))
        distinct_kmer_index = { kmer:i for (i,kmer) in enumerate(distinct_kmers) }
        prefix_to_graph = defaultdict(list)

        for i,k_mer in enumerate(k_mers):
            if k_mer == "ATTTTTTTATTTATTAAAAAAAATTTTTTT":
                print("RARO A")
            if k_mer == "TTTTTTTATTTATTAAAAAAAATTTTTTTT":
                print("RARO B")
            prefix_to_graph[k_mer[:-1]].append(distinct_kmer_index[k_mer])

        graph = []
        for i, k_mer1 in enumerate(distinct_kmers):
            if debug and i % 1000 == 0:
                print(i,"/",len(distinct_kmers))
            
            adyacencias = prefix_to_graph[k_mer1[1:]].copy()
            graph.append(adyacencias)

        return cls(graph, distinct_kmers)

    @classmethod
    def from_overlap_pares(cls, kd_mers, debug=False):
            distinct_kdmers = list(set(kd_mers))
            distinct_kdmer_index = { kmer:i for (i,kmer) in enumerate(distinct_kdmers) }
            prefixes_to_graph = defaultdict(list)
            for i,(kd_mer_1, kd_mer_2) in enumerate(kd_mers):
                prefixes_to_graph[(kd_mer_1[:-1],kd_mer_2[:-1])].append(distinct_kdmer_index[(kd_mer_1, kd_mer_2)])
    
            graph = []
            for i, (kd_mer_1, kd_mer_2) in enumerate(distinct_kdmers):
                if debug and i % 1000 == 0:
                    print(i,"/",len(distinct_kdmers))
                adyacencias = prefixes_to_graph[(kd_mer_1[1::],kd_mer_2[1::])].copy()
                graph.append(adyacencias)
    
            return cls(graph, distinct_kdmers)

    # la comentamos pq no se usa
        # @classmethod
        # def debrujin_from_text(cls, k, text):
        #     k_mers = set()
        #     for i in range(len(text) - k + 2):
        #         k_mers.add(text[i:i+k-1])
        #     k_mers = list(k_mers)
        #     print(k_mers)
        #     adyacencias = [[] for i in range(len(k_mers))]
        #     for i in range(len(text) - k + 1):
        #         solapamiento1 = text[i:i+k-1]
        #         solapamiento2 = text[i+1:i+k]
        #         adyacencias[k_mers.index(solapamiento1)].append(k_mers.index(solapamiento2))
        #     return cls(adyacencias, k_mers)
         
    
    def in_degree(self):
        in_degree_list = [0 for x in self.adyacencias]
        for nodo in self.adyacencias:
            for adyacente in nodo:
                in_degree_list[adyacente]+=1
        return in_degree_list

    def out_degree(self):
        return [len(x) for x in self.adyacencias]
                
    # une un nodo final y terminal del grafo. supone que son unicos
    def unir_puntas(self) -> int:
        min_indeg = np.inf
        min_outdeg = np.inf
        #print(list(zip(self.in_degree(),self.out_degree())))
        print("a")
        a=list(zip(self.in_degree(),self.out_degree()))
        print("b")
        counts = Counter(a)
        
        print(counts)

        for (i, (indeg, outdeg)) in enumerate(zip(self.in_degree(), self.out_degree())):
            if indeg != outdeg:
                print(i)
                print(indeg, outdeg, self.k_mers[i],self.adyacencias[i], [self.k_mers[j] for j in self.adyacencias[i]])
                print(indeg, outdeg, "\\n*".join(list(self.k_mers[i])), ["\n*".join(list(self.k_mers[j])) for j in self.adyacencias[i]])
            if indeg > outdeg and outdeg < min_outdeg:
                min_outdeg = outdeg
                punta_final = i
            elif outdeg > indeg and indeg < min_indeg:
                min_indeg = indeg
                punta_inicial = i
        #print(punta_inicial, punta_final,self.k_mers[punta_inicial],self.k_mers[punta_final] )
        print("d")
        self.adyacencias[punta_final].append(punta_inicial)
        print("e")
        return punta_inicial



    #Devuelve la matriz* de un grafo para calcular el numero de ciclos eulerianos del teorema BEST
    def matriz_adyacencia_ne_conInDegree(self):
        
        matriz = np.zeros((len(self.k_mers), len(self.k_mers)), dtype=int)

        for i, nodo in enumerate(self.adyacencias):
            for adyacente in nodo:
                matriz[i][adyacente] = -1

        indegree = self.in_degree()
        
        for i in range(len(indegree)):
            matriz[i][i] = indegree[i]

        return matriz

    def count_eulerian_cycles_BEST(self):
        #TODO verificar que sea euleriano primero
        matrizNegadaConInDegree = self.matriz_adyacencia_ne_conInDegree()
        cofactor = np.linalg.det(matrizNegadaConInDegree[1:,1:])
        
        res = cofactor
        for i in range(matrizNegadaConInDegree.shape[0]):
            print(matrizNegadaConInDegree[i][i])
            res = res * factorial(matrizNegadaConInDegree[i][i] - 1)
        #res = int(res)
        print(format(res.astype(int),'.17f'))
        return res
        

    def eulerian_cycle(self):
        ciclo = [0]
        aristas = deepcopy(self.adyacencias)
        nodo = 0
        nodo = aristas[nodo].pop(0)
        while nodo != 0:
            ciclo.append(nodo)
            nodo = aristas[nodo].pop(0)

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

            #ciclo = ciclo[:ciclo.index(nodo_original)] + ciclonuevo + ciclo[ciclo.index(nodo_original):]
            ciclo[ciclo.index(nodo_original):ciclo.index(nodo_original)] = ciclonuevo
        return ciclo


    def print_overlap(self):
        if len(self.k_mers) > 20:
            print("too long will break")
        else:
            for i, k_mer1 in enumerate(self.k_mers):
                print(k_mer1, "->", ",".join([self.k_mers[j] for j in self.adyacencias[i]]))

example_string = "TAATGCCATGGGATGTT"
example_list = [example_string[i:i+3] for i in range(len(example_string)-2)]
example_list212 = [(example_string[i:i+2],example_string[i + 3:i+5]) for i in range(len(example_string)-4)]

def testmain():
    #secuencia = input("input txt\n")
    #k = int(input("input len\n"))
    #print(combinaciones_k(secuencia, k))
    #print("Example string: ", example_string)
    #print("Example list: ", example_list)
    #print("StringFromPath(example_list): ", stringFromPath(example_list))
    #print("")
    #k_mers = combinaciones_k(example_string, 3)
    #graph.from_overlap(k_mers).print_overlap()
    print("overlap:")
    b = graph.debrujin_from_text(3,example_string)
    print("GRAFO SIN UNIR PUNTAS:")
    b.print_overlap()
    b.unir_puntas()
    print("\n\nGRAFO CON UNIR PUNTAS:")
    b.print_overlap()
    print("\n\n")

#
#    #est_eulerian = [
    #    [2,3],
    #    [0,4],
    #    [3],
    #    [0,5],
    #    [5],
    #    [1,6],
    #    [1],

    test_eulerian = [
        [1],
        [2,3],
        [0,1],
        [2]
    ]      
    test_eulerian1 = [
            [1,2], 
            [0,2],
            [0,1]
        ]

    test_eulerian2 = [
            [1],
            [2],
            [3],
            [0]
        ]   
    
    test_eulerian_names = list(map(str,range(3)))
    #   ([[0, 1, 0, 0],
    #   [0, 0, 1, 1],
    #   [1, 1, 0, 0],
    #   [0, 0, 1, 0]])


            
    est_eulerian_names = list(map(str,range(7)))

    a = graph(test_eulerian1, test_eulerian_names)
    a.print_overlap()
    print(a.matriz_adyacencia_ne_conInDegree())
    print("Cantidad de ciclos eulerianos: ", a.count_eulerian_cycles_BEST())
    
    #print(a.eulerian_cycle())

    #print("\n\ncombinaciones de pares", combinaciones_de_pares(example_string, 3, 1))
    #print("example_strin_212", example_list212)
    #print("example_strin_nor", example_string)
    #print(stringFromPathPares(example_list21a))
    
    
if __name__ == "__main__":
    testmain()

    