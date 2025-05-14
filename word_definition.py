from CoreServices import DictionaryServices

def lookup_word(word):
    """Looks up a word in the macOS Dictionary.
    Args:
        word (str): The word to look up.
    Returns:
        str: The definition of the word, or None if not found.
    """
    try:
        wordrange = (0, len(word))
        definition = DictionaryServices.DCSCopyTextDefinition(None, word, wordrange)
        if definition:
            return definition
        else:
            return None
    except Exception as e:
        print(f"Error looking up word: {e}")
        return None
