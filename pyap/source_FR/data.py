# -*- coding: utf-8 -*-

"""
    pyap.source_FR.data
    ~~~~~~~~~~~~~~~~~~~~

    This module provides regular expression definitions required for
    detecting French addresses.

    The module is expected to always contain 'full_address' variable containing
    all address parsing definitions.

    :copyright: (c) 2023 by Hong Quan Tran.
    :license: MIT, see LICENSE for more details.
"""


'''Numerals from one to nine
Note: here and below we use syntax like '[Oo][Nn][Ee]'
instead of '(one)(?i)' to match 'One' or 'oNe' because
Python Regexps don't seem to support turning On/Off
case modes for subcapturing groups.
'''
zero_to_nine = r"""
                                (?:
                                    [Zz][Ee][Rr][Oo]\ |[Oo][Nn][Ee]\ |[Tt][Ww][Oo]\ |
                                    [Tt][Hh][Rr][Ee][Ee]\ |[Ff][Oo][Uu][Rr]\ |
                                    [Ff][Ii][Vv][Ee]\ |[Ss][Ii][Xx]\ |
                                    [Ss][Ee][Vv][Ee][Nn]\ |[Ee][Ii][Gg][Hh][Tt]\ |
                                    [Nn][Ii][Nn][Ee]\ |[Tt][Ee][Nn]\ |
                                    [Ee][Ll][Ee][Vv][Ee][Nn]\ |
                                    [Tt][Ww][Ee][Ll][Vv][Ee]\ |
                                    [Tt][Hh][Ii][Rr][Tt][Ee][Ee][Nn]\ |
                                    [Ff][Oo][Uu][Rr][Tt][Ee][Ee][Nn]\ |
                                    [Ff][Ii][Ff][Tt][Ee][Ee][Nn]\ |
                                    [Ss][Ii][Xx][Tt][Ee][Ee][Nn]\ |
                                    [Ss][Ee][Vv][Ee][Nn][Tt][Ee][Ee][Nn]\ |
                                    [Ee][Ii][Gg][Hh][Tt][Ee][Ee][Nn]\ |
                                    [Nn][Ii][Nn][Ee][Tt][Ee][Ee][Nn]\ 
                                )
"""

# Numerals - 10, 20, 30 ... 90
ten_to_ninety = r"""
                                (?:
                                    [Tt][Ee][Nn]\ |[Tt][Ww][Ee][Nn][Tt][Yy]\ |
                                    [Tt][Hh][Ii][Rr][Tt][Yy]\ |
                                    [Ff][Oo][Rr][Tt][Yy]\ |
                                    [Ff][Oo][Uu][Rr][Tt][Yy]\ |
                                    [Ff][Ii][Ff][Tt][Yy]\ |[Ss][Ii][Xx][Tt][Yy]\ |
                                    [Ss][Ee][Vv][Ee][Nn][Tt][Yy]\ |
                                    [Ee][Ii][Gg][Hh][Tt][Yy]\ |
                                    [Nn][Ii][Nn][Ee][Tt][Yy]\ 
                                )
"""

# One hundred
hundred = r"""
                                (?:
                                    [Hh][Uu][Nn][Dd][Rr][Ee][Dd]\ 
                                )
"""

# One thousand
thousand = r"""
                                (?:
                                    [Tt][Hh][Oo][Uu][Ss][Aa][Nn][Dd]\ 
                                )
"""

part_divider = r'(?: [\,\ \.\-]{0,3}\,[\,\ \.\-]{0,3} )'
space_pattern = r'(?: [\ \t]{1,3} )'  # TODO: use \b for word boundary and \s for whitespace

'''
Regexp for matching street number.
Street number can be written 2 ways:
1) Using letters - "One thousand twenty two"
2) Using numbers
   a) - "1022"
   b) - "85-1190"
   c) - "85 1190"


==> LIMITING THE OPTION TO ONLY 1 WAY OF WRITTING STREET NUMBER -> USING NUMBER FOR FRENCH
'''
street_number = r"""
                    (?P<street_number>
                        (?:
                            (?:
                                [Nn][Uu][Mm][Bb][Ee][Rr]|
                                [Nn][RrOo]\.?|
                                [Nn][Uu][Mm]\.?|
                                #
                            )
                            {space}?
                        )?
                        (?:
                            (?:
                                [Aa][Nn][Dd]\ 
                                |
                                {thousand}
                                |
                                {hundred}
                                |
                                {zero_to_nine}
                                |
                                {ten_to_ninety}
                            ){from_to}
                            |
                            (?:
                                \d{from_to} 
                                (?: {space}? [A-Za-z] (?![A-Za-z\d]]) )? 
                                (?!\d)
                                (?:{space}?\-{space}?\d{from_to} (?: {space}? [A-Za-z] (?![A-Za-z\d]) )? )?
                            )
                        )
                        {space}?
                    )  # end street_number
""".format(
    thousand=thousand,
    hundred=hundred,
    zero_to_nine=zero_to_nine,
    ten_to_ninety=ten_to_ninety,
    space=space_pattern,
    from_to='{1,5}',
)

'''
Regexp for matching street name.
In "Hoover Boulevard", "Hoover" is a street name
Seems like the longest US street is 'Northeast Kentucky Industrial Parkway' - 31 charactors
https://atkinsbookshelf.wordpress.com/tag/longest-street-name-in-us/
'''
street_name = r"""
                    (?P<street_name>
                        (?(street_number)           # If street_number has been found, then digits can
                            [a-zA-Z0-9\ \.]{3,31}   # be in the street otherwise no digits are allowed.
                            |                       # This aims to prevent street_name matching everything before the
                            [a-zA-Z\ \.]{3,31}      # address as well as the number.
                        )
                    )
"""

post_direction = r"""
                    (?P<post_direction>
                        (?:
                            [Nn][Oo][Rr][Tt][Hh]\ |
                            [Ss][Oo][Uu][Tt][Hh]\ |
                            [Ee][Aa][Ss][Tt]\ |
                            [Ww][Ee][Ss][Tt]\ 
                        )
                        |
                        (?:
                            NW\ |NE\ |SW\ |SE\ 
                        )
                        |
                        (?:
                            N\.?\ |S\.?\ |E\.?\ |W\.?\ 
                        )
                    )  # end post_direction
"""

# Regexp for matching street type
import string
import re
from unidecode import unidecode

street_type_list = [
    "Allée", 'ALL',
    'Avenue', 'AV',
    'Boulevard', 'BD',
    'Centre', 'CTRE',
    'Centre Commercial', 'CCAA',
    'Immeuble', 'Immeubles', 'IMM',
    'Impasse', 'IMP',
    'Lieu-dit', 'Lieu dit', 'LD', 'Lieudit'
    'Lotissement', 'LOT',
    'Passage', 'PAS', 
    'Place', 'PL',
    'Résidence', 'RES',
    'Rond-Point', 'Rond Point', 'RondPoint', 'RPT'
    'Route', 'RTE',
    'Square', 'SQ',
    'Village', 'VLGE',
    "Zone d'activité", 'ZA',
    "Zone d'activité concerté", "ZAC",
    "Zone d'activité différé", "ZAD",
    "Zone industrielle", "ZI"
    'Chemin', 'CHEM',
    'Sentier', 'SENT',
    
    # outside the link
    'Montée',
    'Ruelle',
]

def street_type_list_to_regex(street_type_list):
    """Converts a list of street types into a regex"""
    street_types = '|'.join(set(street_type_list)).lower()
    
    for letter in string.ascii_lowercase:
        street_types = street_types.replace(letter, '[{upper}{lower}]'.format(upper=letter.upper(), lower=letter))
        
    for letter in 'éèêëçîïàâäôöùûüÿ':
        street_types = street_types.replace(
            letter, 
            '[{upper}{lower}{upper_norm}{lower_norm}]'.format(
                upper=letter.upper(), 
                lower=letter, 
                upper_norm=unidecode(letter).upper(),
                lower_norm=unidecode(letter).lower()
            )
        )
        
    street_types = re.sub(r"[ '-]", "[ '-]?", street_types)

    # Use \b to check that there are word boundaries before and after the street type
    # Optionally match zero to two of " ", ",", or "." after the street name
        
    street_types = street_types.replace('|', r'\b{div}|\b')
    street_types = r'\b' + street_types + r'\b{div}'
    
    
    return street_types.format(
        div=r'[\.\ ,]{0,2}',
    )

floor = r"""
                    (?P<floor>
                        (?:
                        \d+[A-Za-z]{0,2}\.?\ [Ff][Ll][Oo][Oo][Rr]\ 
                        )
                        |
                        (?:
                            [Ff][Ll][Oo][Oo][Rr]\ \d+[A-Za-z]{0,2}\ 
                        )
                    )  # end floor
"""

building = r"""
                    (?P<building_id>
                        (?:
                            (?:[Bb][Uu][Ii][Ll][Dd][Ii][Nn][Gg])
                            |
                            (?:[Bb][Ll][Dd][Gg])
                        )
                        \ 
                        (?:
                            (?:
                                [Aa][Nn][Dd]\ 
                                |
                                {thousand}
                                |
                                {hundred}
                                |
                                {zero_to_nine}
                                |
                                {ten_to_ninety}
                            ){{1,5}}
                            |
                            \d{{0,4}}[A-Za-z]?
                        )
                        \ ?
                    )  # end building_id
""".format(
    thousand=thousand,
    hundred=hundred,
    zero_to_nine=zero_to_nine,
    ten_to_ninety=ten_to_ninety,
)

occupancy = r"""
                    (?P<occupancy>
                        (?:
                            (?:
                                # Suite
                                [Ss][Uu][Ii][Tt][Ee]|[Ss][Tt][Ee]\.?
                                |
                                # Studio
                                [Ss][Tt][Uu][Dd][Ii][Oo]|[Ss][Tt][UuDd]\.?
                                |
                                # Apartment
                                [Aa][Pp][Tt]\.?|[Aa][Pp][Aa][Rr][Tt][Mm][Ee][Nn][Tt]
                                |
                                # Room
                                [Rr][Oo][Oo][Mm]|[Rr][Mm]\.?
                                |
                                # Flat
                                [Ff][Ll][Aa][Tt]
                                |
                                \#
                            )
                            {space}?
                            (?:
                                [A-Za-z\#\&\-\d]{{1,7}}
                            )?
                        )
                        {space}?
                    )  # end occupancy
""".format(
    space=space_pattern,
)

po_box = r"""
                    (?:
                        [Pp]\.? {space}? [Oo]\.? {space}? ([Bb][Oo][Xx]{space}?)?\d+
                    )
""".format(
    space=space_pattern,
)

full_street = r"""
        (?:
            (?P<full_street>
    
                (?:
                    {po_box} {part_divider}?  # TODO: maybe remove the '?' on the part_dividers is mismatch address parts 
                )?
                (?:
                    {floor} {part_divider}?
                )?
                (?:
                    {occupancy} {part_divider}?
                )?
                (?:
                    {building} {part_divider}?
                )?
                
                (?:
                    (?: {street_number} {space} )
                    |
                    (?! \d{{}} ) 
                    
                )?
                (?:{street_name} )
                (?:{space} {street_type} {space}?)? 
            )
        )  # end full_street
""".format(
    street_number=street_number,
    street_name=street_name,
    street_type=street_type,
    post_direction=post_direction,
    floor=floor,
    building=building,
    occupancy=occupancy,
    po_box=po_box,
    part_divider=part_divider,
    space=space_pattern,
)

postal_code = r"""
                (?P<postal_code>
                    (?:\d{5})
                )
                """

def commune_list_to_regex(street_type_list):
    """Converts a list of street types into a regex"""
    
    special_cases = {
        'e' : 'éèêëÉÈÊË',
        'c' : 'Ç',
        'i' : 'îïÎÏ',
        'a' : 'àâäÀÂÄ',
        'o' : 'ôöùÔÖÙ',
        'u' : 'ûüÛÜ',
        'y' : 'Ÿ'
    }
    
    street_types = '|'.join(set(street_type_list)).lower()
    
    for letter in string.ascii_lowercase:
        street_types = street_types.replace(
            letter, 
            '[{upper}{lower}{special_cases}]'.format(
                upper=letter.upper(), 
                lower=letter,
                special_cases=special_cases.get(letter, '')
            )
        )
        
    street_types = re.sub(r"[ '-]", "[ '-]?", street_types)

    # Use \b to check that there are word boundaries before and after the street type
    # Optionally match zero to two of " ", ",", or "." after the street name
        
    street_types = street_types.replace('|', r'\b{div}|\b')
    street_types = r'\b' + street_types + r'\b{div}'
    
    
    return street_types.format(
        div=r'[\.\ ,]{0,2}',
    )

import pandas as pd 

# https://www.data.gouv.fr/fr/datasets/base-officielle-des-codes-postaux/
codes_postal_df = pd.read_csv('codes_postsal.csv', sep=';' , encoding='latin-1')
communes = codes_postal_df.Nom_de_la_commune.tolist()


country = r"""
        (?P<country>
            (?:[Tt][Hh][Ee]\ *)?[Uu][Nn][Ii][Tt][Ee][Dd]\ *[Kk][Ii][Nn][Gg][Dd][Oo][Mm]\ *[Oo][Ff]\ *(?:[Gg][Rr][Ee][Aa][Tt]\ *)?[Bb][Rr][Ii][Tt][Aa][Ii][Nn](?:\ *[Aa][Nn][Dd]\ *[Nn][Oo][Rr][Tt][Hh][Ee][Rr][Nn]\ *[Ii][Rr][Ee][Ll][Aa][Nn][Dd])?|
            (?:[Gg][Rr][Ee][Aa][Tt]\ *)?[Bb][Rr][Ii][Tt][Aa][Ii][Nn](?:\ *[Aa][Nn][Dd]\ *[Nn][Oo][Rr][Tt][Hh][Ee][Rr][Nn]\ *[Ii][Rr][Ee][Ll][Aa][Nn][Dd])?|
            (?:[Tt][Hh][Ee]\ *)?[Uu][Nn][Ii][Tt][Ee][Dd]\ *[Kk][Ii][Nn][Gg][Dd][Oo][Mm]|
            (?:[Nn][Oo][Rr][Tt][Hh][Ee][Rr][Nn]\ *)?[Ii][Rr][Ee][Ll][Aa][Nn][Dd]|
            [Ee][Nn][Gg][Ll][Aa][Nn][Dd]|
            [Ss][Cc][Oo][Tt][Ll][Aa][Nn][Dd]|
            [Ww][Aa][Ll][Ee][Ss]|
            [Cc][Yy][Mm][Rr][Uu]|
            [Gg][Bb]|
            [Uu][Kk]|  
            [Nn]\.?\ *[Ii]\.?
        )  # end country
"""

full_address = r"""
    (?P<full_address>
        {full_street} 
        {part_divider}? {postal_code} 
        {part_divider}? {communes} 
    )  # end full_address
""".format(
    full_street=full_street,
    part_divider=part_divider,
    postal_code=postal_code,
    communes = commune_list_to_regex(communes)
)



# add not appt / app
# chinh viet tat ten commune saint/st ....
# commune co hay ko cung duoc de range cove duoc rong hon 
# 


