import os
import parser
from musicxml import *

FOLDER = "musicxml"
KEY_SYMBOL = "@"
OUT = "sequences.csv"

NOTES = [
    "C",
    "Db",
    "D",
    "Eb",
    "E",
    "F",
    "Gb",
    "G",
    "Ab",
    "A",
    "Bb",
    "B"
]

def int_to_note(x):
    return NOTES[x % 12]

def get_musicxml_at_path(path) -> XMLScorePartwise:
    return parser.parse_musicxml(path)
def get_key_string(key_xml: XMLKey):
    val = key_xml.find_child(XMLFifths).value_
    val = val * 7
    mode = key_xml.find_child(XMLMode).value_
    match mode:
        case "major": return KEY_SYMBOL + int_to_note(val)
        case "minor": return KEY_SYMBOL + int_to_note(val - 3) + "m"
        case _: raise Exception("Mode " + mode + " unknown")
        
def get_harmony_string(harm_xml: XMLHarmony):
    root = harm_xml.find_child(XMLRoot)
    step = root.find_child(XMLRootStep).value_
    alter = root.find_child(XMLRootAlter)
    if alter != None:
        if alter.value_ == -1: step += "b"
        elif alter.value_ == 1: step += "#"
    return step + harm_xml.find_child(XMLKind).attributes["text"]


def main():
    with open(OUT, "w") as outfile:
        for filename in os.listdir(FOLDER):
            path = os.path.join(FOLDER, filename)
            if os.path.isfile(path):
                xml = get_musicxml_at_path(path)
                name = xml.find_child(XMLWork).find_child(XMLWorkTitle).value_
                name = name.replace(", ", " ").replace(" ", "-")
                outfile.write(name + ",")
                measures = xml.find_child(XMLPart).find_children(XMLMeasure)
                for measure in measures:
                    attrs = measure.find_child(XMLAttributes)
                    if attrs != None:
                        key = attrs.find_child(XMLKey)
                        if key != None: outfile.write(get_key_string(key) + ", ")
                    for harmony in measure.find_children(XMLHarmony):
                        h = get_harmony_string(harmony)
                        outfile.write(h + ", ")
                print("Read " + name)
                outfile.write("\n")
            
                
            

if __name__ == "__main__":
    main()
