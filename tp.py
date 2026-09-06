import secuencias as sec

# 


def carsonellaRuddiiMain():
    with open("CarsonellaRuddii.txt") as genome:
        genome = "".join(genome.read().splitlines())
        
    genome2 = "TAATGCCATGGGATGTT"
    k_mers = sec.combinaciones_k(genome2,4)
    debrujin_graph = sec.graph.from_overlap(k_mers)
    debrujin_graph.unir_puntas()



if __name__ == "__main__":
    carsonellaRuddiiMain()

