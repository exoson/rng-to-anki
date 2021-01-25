import glob
import os

import genanki

f = glob.glob("ranges\\*.rng")

deck = genanki.Deck(
    1234,
    "Preflop Ranges",
)

model = genanki.Model(
    1234,
    "Preflop Quiz model",
    fields=[
        {"name": "Question"},
        {"name": "Answer"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Question}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ],
)
postions = ["LJ", "HJ", "CO", "BU", "SB", "BB"]
#change who's first in
first_pos = "BU"

for x in range(len(f)):
    file_name = f[0]
    sizes = file_name.split("\\")[-1].split(".")
    range_name = ""
    abc = postions.index(first_pos)
    open_raiser = postions[abc:]
    for _ in range(len(sizes)-1):
        if sizes[0] == "0":
            range_name += open_raiser[0] + " fold "
            open_raiser.pop(0)
            sizes.pop(0)
        elif sizes[0] == "1":
            range_name += open_raiser[0] + " call "
            sizes.pop(0)
            open_raiser.append(open_raiser[0])
            open_raiser.pop(0)
        elif sizes[0] == "3":
            range_name += open_raiser[0] + " jam "
            open_raiser.pop(0)
            sizes.pop(0)
        elif sizes[0] == "5":
            range_name += open_raiser[0] + " min raise "
            open_raiser.append(open_raiser[0])
            open_raiser.pop(0)
            sizes.pop(0)
        else:
            range_name += open_raiser[0] + " raise " + sizes[0][2:] + "% "
            open_raiser.append(open_raiser[0])
            open_raiser.pop(0)
            sizes.pop(0)
    lines = [line.rstrip('\n') for line in open(file_name)]
    while len(lines) > 0:
        hand = lines.pop(0)
        value = lines.pop(0).split(";", maxsplit=1)[0]

        question = "{} {}".format(range_name, hand)
        note = genanki.Note(
            model=model,
            fields=[question, value]
        )
        deck.add_note(note)
    f.pop(0)

genanki.Package(deck).write_to_file("output.apkg")
