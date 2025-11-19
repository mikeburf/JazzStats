import chord_graph
import reader



conv = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11
}

rel = [
    "I",
    "bII",
    "II",
    "bIII",
    "III",
    "IV",
    "bV",
    "V",
    "bVI",
    "VI",
    "bVII",
    "VII"
]

GRAPH_OUT = "graph.txt"


def main():
    G = chord_graph.ChordGraph()


    with open(reader.OUT, "r") as csv:

        while True:
            line = csv.readline()
            if not line: break

            key = 0
            c = 0
            lastChord = None
            for field in line.split(","):
                field = field.strip()

                if not field: break

                if c == 0:
                    pass
                elif c == 1:
                    key = conv[field[1]]
                    ptr = 2
                    if ptr < len(field):
                        if field[ptr] == "b":
                            key -= 1
                            ptr += 1
                        elif field[ptr] == "#":
                            key += 1
                            ptr += 1
                else:
                    root = conv[field[0]]
                    ptr = 1
                    if ptr < len(field):
                        if field[ptr] == "b":
                            root -= 1
                            ptr += 1
                        elif field[ptr] == "#":
                            root += 1
                            ptr += 1
                    relative_root = (root - key) % 12
                    chord = rel[relative_root] + field[ptr:]
                    if lastChord != None:
                        G.add_occurrence(lastChord)
                        if lastChord != chord:
                            G.add_edge(lastChord, chord)
                    
                    lastChord = chord
                c += 1
    G.finish()
    with open(GRAPH_OUT, "w") as outfile:
        outfile.write(G.debug())


if __name__ == "__main__":
    main()
