from hashids import Hashids

# Salt used to generate unique, non-sequential short codes
SALT = "X9v$8kLpQ"

# Initialize Hashids instance with minimum length of 6
hashids = Hashids(min_length=6, salt=SALT)


def encode_id(id):
    """
    Encode a numeric database ID into a short, obfuscated code.
    
    Args:
        id (int): Database ID to encode.
    
    Returns:
        str: Encoded short code.
    """
    return hashids.encode(id)


def decode_id(code):
    """
    Decode a short code back to the original numeric database ID.
    
    Args:
        code (str): Short code to decode.
    
    Returns:
        int or None: Original database ID if valid, otherwise None.
    """
    ids = hashids.decode(code)
    return ids[0] if ids else None
