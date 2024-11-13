desenho_forca = {
    0:"""
     __
    |  |
    |  
    | 
    |
    """,
    1:"""
     __
    |  |
    |  O
    | 
    |
    """,
    2:"""
     __
    |  |
    |  O
    |  |
    |
    """,
    3:"""
     __
    |  |
    |  O
    | /|
    |
    """,
    4:"""
     __
    |  |
    |  O
    | /|\\
    |
    """,

    5:"""
     __
    |  |
    |  O
    | /|\\
    | /
    """,

    6:"""
     __
    |  |
    |  O
    | /|\\
    | / \\
    """,
}

def get_desenhos_forca(attempts: int) -> str:
    return desenho_forca.get(attempts,0)