#       FRA Kryptokluring 1 2023-12-05
#
#       Joakim Argillander, Linköpings universitet
#
#       joakim.argillander@liu.se
#       joakim@argillander.se
#       www.argillander.se



import string


class Node:
    """
    Klass för att representera den trädstruktur som skapas. 
    Binärt träd används för att representera de två val som kan göras vid avkodningen. 
    T.ex. behandlas det numeriska värdet 12 som antingen "1" och "2", motsvarande "A" och "B", 
    eller som värdet "12" motsvarande "L".
    """

    def __init__(self, data):
        self.data = data
        self.char = None
        self.left = None
        self.right = None

    def add_left_child(self, child):
        self.left = child

    def add_right_child(self, child):
        self.right = child

    def is_leaf(self):
        return (self.left == None) and (self.right == None)




def make_tree(tree, message, max_char_code=29):
    """ 
    Genererar det binära trädet som ges av telegramtexten som omvandlats till 
    """
    if not message:
        return
    else:
        a = message[:1]
        b = message[:2]
        child_1 = Node(int(a))
        if len(b) == 2:
            # Only consider case when two-digit exist
            child_2 = Node(int(b))
        else:
            child_2 = None

        #child_1.char = get_char_from_idx(int(a), )
        #child_2.char = get_char_from_idx(int(b), )
        #tree.children.append(child_1)
        #tree.children.append(child_2)
        tree.left = child_1
        tree.right = child_2
        if int(b) > max_char_code:
            #print("Discarding ", int(b))
            return make_tree(child_1, message[1:]), make_tree(child_2, None)
        return make_tree(child_1, message[1:]), make_tree(child_2, message[2:])


def get_char_from_idx(index):
    """
    Returnerar den i:te bokstaven från alfabetet. 
    OBS: Genom försök upptäcks att 'w' inte ingår i teckenuppsättningen.
    """

    alphabet = "abcdefghijklmnopqrstuvxyzåäö".upper()

    if type(index) is not int:
        return ""
    if index < 0:
        return "."
    elif index > len(alphabet):
        return "*"
    return alphabet[(index) % len(alphabet)]


def find_string_list(node, s, results):
    """ 
    Traverserar trädstrukturen och genererar kandidatsträngar för telegrammets ord.
    """
    if not node:
        return
    if node.is_leaf():
        results.append(s+get_char_from_idx(node.data))
        return
    find_string_list(node.left, s + get_char_from_idx(node.data), results)
    find_string_list(node.right, s + get_char_from_idx(node.data), results)


def decipher(msg, filter_with_wordlist=False):
    """
    Huvudfunktion för dekrypteringen av chiffertexten. 
    Kan filtrera kandidatord med ordlista för att eliminera icke-giltiga ord.
    """

    for ciphertext in msg.split(" "):
        print("Deciphering \"{}\"".format(ciphertext))
        result_list = []

        root = Node("R")
        make_tree(root, ciphertext)
        #find_strings(root, "", os=cipher)
        find_string_list(root, "", result_list)
        #print("Possible solutions:", len(result_list))

        if filter_with_wordlist:
            result_list = filter_wordlist(result_list, "./swe_wordlist")

        print(result_list)
        print("\nFound {} solutions for \"{}\"\n\n".format(len(result_list), ciphertext)) 


def filter_wordlist(candidates, wordlistfile):
    """
    Filtrera på vanligaste svenska orden. 
    Ordlista från https://github.com/martinlindhe/wordlist_swedish
    """

    wordlist = "./swe_wordlist"

    wl = []
    out = []
    with open(wordlist, "r") as f:
        wl = f.read().splitlines()
        
    for x in candidates:
        for w in wl:
            if w in x:
                out.append(x)
    
    for x in candidates: 
       if x.lower() in wl: 
            out.append(x)

    # Filter out duplicates
    out = set(out)
    out = list(out)
    return out


def convert_message_to_alphabet_indices(telegram):
    """
    Omvandlar det givna telegrammet till en sekvens av bokstavsindex.
    D.v.s. telegrammet 'aabc cd' omvandlas till '0012 23'.
    """
    alphabet = string.ascii_lowercase + "åäö"
    telegram_converted = ""
    for c in telegram:
        if c != " ":
            telegram_converted = telegram_converted + str(alphabet.index(c))
        else:
            telegram_converted = telegram_converted + " "
    
    print("Input telegram:", telegram)
    print("Telegram converted to alphabet index:", telegram_converted)
    print(" ")
    return telegram_converted
 


############################################################################

# Det givna telegrammet
telegram = "cabjbhcabibjbdibdgebd bebjibbbbbhcgcbabbig fchbh cbibdbjebhbehbecb"

# Telegrammet omvandlas till bokstavens index i alfabetet för att skapa en numerisk sekvens per ord
telegram_converted = convert_message_to_alphabet_indices(telegram)


# Skapa en trädstruktur för att representera alla sätt två siffror kan tolkas, tillskriv en bokstav 
# till den bokstavskoden, och sedan traversera trädet för att finna kandidatord. 
# Utan att veta hur långa klartextorden är så är alla kandidatord initialt lika giltig, och filtrering (antingen maskinell eller manuell)
# bör göras. Filtrering kan göras både baserat på endast svenska ord, samt korrespondensens förmodade kontext.

# I detta fall har filtrering ej varit nödvändig, då orden i meddelandets klartext synts i print-output, 
# men om filtrering ska implementeras bör s.k. 'fuzzy filtering' användas för att hantera sammansatta ord
# och ord som är del av andra ord (t.ex. att ordet 'graf' återfinns i 'kryptografi').

# Valfritt: Filtrera med en ordlista av vanliga svenska ord.
decipher(telegram_converted, filter_with_wordlist=False)

# Efter manuell inspektion av möjliga kandidatord, samt givet att telegrammets sammanhang
# förmodligen kan antas vara av militär natur, ges att telegrammet avkodas till
# "UTRUSTNINGEN OTILLRÄCKLIG FÖR VINTERBEHOV"


# /Joakim Argillander


