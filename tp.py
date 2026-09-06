import secuencias as sec

# 
def rotar_ciclo_hasta(ciclo, nodo_inicial):
    #while(ciclo[0]!=inicial) pop push
    nodo_inicial_pos = ciclo.index(nodo_inicial)
    return ciclo[nodo_inicial_pos:] + ciclo[:nodo_inicial_pos]

def carsonellaRuddiiMain():
    with open("CarsonellaRuddii.txt") as genome:
        genome = "".join(genome.read().splitlines())
        
    genome2 = "ACAAAACTTTCTAAATGTTTTCTAGAAAACATTATTATTGTTGCACCTGGTGATTCATA"
    k_mers = sec.combinaciones_k(genome2,5)

    debrujin_graph = sec.graph.from_overlap(k_mers)
    nodo_inicial = debrujin_graph.unir_puntas()
    debrujin_graph.print_overlap()

    count = debrujin_graph.count_eulerian_cycles_BEST()
    if count > 1:
        print("No es posible reconstruir la secuencia original")
    ciclo = debrujin_graph.eulerian_cycle()

    print( [debrujin_graph.k_mers[i] for i in ciclo])

    ciclo_alineado_al_principio = rotar_ciclo_hasta(ciclo, nodo_inicial)

    k_meros_ordenados = [debrujin_graph.k_mers[i] for i in ciclo_alineado_al_principio]
    print(k_meros_ordenados)
    genoma = sec.stringFromPath(k_meros_ordenados)

    print(genoma)    
    print(genome2)    






if __name__ == "__main__":
    carsonellaRuddiiMain()

