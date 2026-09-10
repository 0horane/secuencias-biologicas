import secuencias as sec

# 
def rotar_ciclo_hasta(ciclo, nodo_inicial):
    #while(ciclo[0]!=inicial) pop push
    nodo_inicial_pos = ciclo.index(nodo_inicial)
    return ciclo[nodo_inicial_pos:] + ciclo[:nodo_inicial_pos]

def carsonellaRuddiiMain():
    with open("CarsonellaRuddii.txt") as genome:
        genome = "".join(genome.read().splitlines())

    k = 30
    d = None
    res = run_test_on_genome(genome[:100000], k, d, debug=False)
    print(res)
    
def run_test_on_genome(genome,k,d=None, debug=False):
    if d == None:
        print("Separando en k_meros")
        k_mers = sec.combinaciones_k(genome,k)
        res = reconstruct_genome_from_kmers(k_mers, debug)
    else:
        print("Separando en kd_meros")
        kd_mers = sec.combinaciones_de_pares(genome,k,d)
        res = reconstruct_genome_from_kdmers(kd_mers,k,d, debug)
    return (res == genome) 

def reconstruct_genome_from_kmers(k_mers, debug=False):
    print("Creando grafo a partir de overlap de k_meros")
    debrujin_graph = sec.graph.from_overlap(k_mers, debug)

    k_meros_ordenados = get_ordered_kmers_from_debrujin_graph(debrujin_graph, debug)
    res = sec.stringFromPath(k_meros_ordenados)
    return res

def reconstruct_genome_from_kdmers(k_mers, k, d, debug=False):
    print("Creando grafo a partir de overlap de kd_meros")
    debrujin_graph = sec.graph.from_overlap_pares(k_mers, debug)

    k_meros_ordenados = get_ordered_kmers_from_debrujin_graph(debrujin_graph, debug)
    res = sec.stringFromPathPares(k_meros_ordenados, k, d)
    return res


def get_ordered_kmers_from_debrujin_graph(debrujin_graph, debug=False):
    if debug:
        print("Grafo sin unir puntas:")
        debrujin_graph.print_overlap()
    print("Uniendo puntas, averiguando nodo inical")
    nodo_inicial = debrujin_graph.unir_puntas()
    
    if debug: 
        print("Contnado ciclos eulerianos")

        count = debrujin_graph.count_eulerian_cycles_BEST()
        if count > 1:
            print("No es posible reconstruir la secuencia original")

    print("Calculando ciclo euleriano")
    ciclo = debrujin_graph.eulerian_cycle()

    if debug:
        print( [debrujin_graph.k_mers[i] for i in ciclo])

    print("Rotando ciclo para iniciar donde corresponde")
    ciclo_alineado_al_principio = rotar_ciclo_hasta(ciclo, nodo_inicial)

    k_meros_ordenados = [debrujin_graph.k_mers[i] for i in ciclo_alineado_al_principio]
    return k_meros_ordenados
   






if __name__ == "__main__":
    carsonellaRuddiiMain()

