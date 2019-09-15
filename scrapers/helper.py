"""This file contains helper functions used by the scrapers"""

def fix_title(title):
    """This function takes a title and capitalizes it, 
       even if the word starts with a quotation mark"""

    quotations = ["'", "‘"]
    fixed_title = []

    for word in title.split():
        if word[0] in quotations:
            fixed_word = word[0] + word[1].upper() + word[2:]
            fixed_title.append(fixed_word)

        else:
            fixed_title.append(word.capitalize())
    
    return " ".join(fixed_title)
        