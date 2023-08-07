part_divider = r"(?: [\,\ \.\-]{0,3}\,[\,\ \.\-]{0,3} )"
space_pattern = (
    r"(?: [\ \t]* )"  # TODO: use \b for word boundary and \s for whitespace
)

"""
Regexp for matching street number.
Street number can be written 2 ways:
1) Using letters - "One thousand twenty two"
2) Using numbers
   a) - "1022"
   b) - "85-1190"
   c) - "85 1190"


==> LIMITING THE OPTION TO ONLY 1 WAY OF WRITTING STREET NUMBER -> USING NUMBER FOR FRENCH
"""
street_number = r"""(?P<street_number>(?:\d{from_to}){space}?)""".format(
    space=space_pattern,
    from_to="{1,5}",
)

"""
Regexp for matching street name.
In "Hoover Boulevard", "Hoover" is a street name
Seems like the longest US street is 'Northeast Kentucky Industrial Parkway' - 31 charactors
https://atkinsbookshelf.wordpress.com/tag/longest-street-name-in-us/
"""
street_name = r"""(?P<street_name>[a-zA-Z0-9À-ÿ\ \.]{3,40})"""

# Regexp for matching street type
import string
import re
from unidecode import unidecode

street_type_list = [
    "Allée",
    "ALL",
    "Avenue",
    "AV",
    "Boulevard",
    "BD",
    "Centre",
    "CTRE",
    "Centre Commercial",
    "CCAA",
    "Immeuble",
    "Immeubles",
    "IMM",
    "Impasse",
    "IMP",
    "Lieu-dit",
    "Lieu dit",
    "LD",
    "Lieudit" "Lotissement",
    "LOT",
    "Passage",
    "PAS",
    "Place",
    "PL",
    "Résidence",
    "RES",
    "Rond-Point",
    "Rond Point",
    "RondPoint",
    "RPT" "Route",
    "RTE",
    "Square",
    "SQ",
    "Village",
    "VLGE",
    "Zone d'activité",
    "ZA",
    "Zone d'activité concerté",
    "ZAC",
    "Zone d'activité différé",
    "ZAD",
    "Zone industrielle",
    "ZI" "Chemin",
    "CHEM",
    "Sentier",
    "SENT",
    # outside the link
    "Montée",
    "Ruelle",
    "Rue"
]


def street_type_list_to_regex(street_type_list):
    """Converts a list of street types into a regex"""
    street_types = "|".join(set(street_type_list)).lower()

    for letter in string.ascii_lowercase:
        street_types = street_types.replace(
            letter, "[{upper}{lower}]".format(upper=letter.upper(), lower=letter)
        )

    for letter in "éèêëçîïàâäôöùûüÿ":
        street_types = street_types.replace(
            letter,
            "[{upper}{lower}{upper_norm}{lower_norm}]".format(
                upper=letter.upper(),
                lower=letter,
                upper_norm=unidecode(letter).upper(),
                lower_norm=unidecode(letter).lower(),
            ),
        )

    street_types = re.sub(r"[ '-]", "[ '-]?", street_types)

    # Use \b to check that there are word boundaries before and after the street type
    # Optionally match zero to two of " ", ",", or "." after the street name

    street_types = street_types.replace("|", r"\b{div}|\b")
    street_types = r"\b" + street_types + r"\b{div}"

    return street_types.format(
        div=r"[\.\ ,]{0,2}",
    )


full_street = r"""(?:
    (?P<full_street>
        (?:
            (?:{street_number}{space})
            |
            (?! \d{{}})
        )?
    )
)  # end full_street
""".format(
    street_number=street_number,
    street_name=street_name,
    street_type=street_type_list_to_regex(street_type_list),
    part_divider=part_divider,
    space=space_pattern,
)

full_street = r"""(?:(?P<full_street>(?:(?:{street_number}|(?! \d{{}}))?(?:{space}{street_type}{space}s?))))""".format(
    street_number=street_number,
    space=space_pattern,
    street_type = street_type_list_to_regex(street_type_list)
)

print(full_street)
print(re.findall(full_street, "123 rue"))
