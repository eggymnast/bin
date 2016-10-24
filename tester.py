def is_match(s):
    s = s.lower()
    return "foil" in s or "3f" in s or "reversal" in s

tests = [
    ("Ioana_SI_4k_&_ALL_foils_70dB_one to six", True),
    ("Ioana_SI_REVERSAL", True),
    ("Ioana_SI_bar", False)
]

for test in tests:
    if is_match(test[0]) != test[1]:
        print("Wrong result on %s" % test[0])
