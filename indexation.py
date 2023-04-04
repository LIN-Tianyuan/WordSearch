import string

# Obtenir des stopwords du fichier
def get_stopwords():
    keywords = []
    # Ouvrir le document des stopwords
    with open('stopwords.txt', 'r') as file:
        lines = file.readlines()
        # Ajouter à la liste
        for line in lines:
            if not line:
                print("Read file End or Error")
                break
            keywords.append(line.strip('\n'))
    return keywords


# Supprimer le stopwords, les chaînes vides et les signes de ponctuation
def index(file):
    keywords = get_stopwords()
    delete_words = []
    with open(file, 'r') as file:
        content = file.read()
        words = content.split()

    punctuations = string.punctuation
    punctuations = punctuations + "’"

    for word in words:
        if ',' in word:
            words.remove(word)
            new_word = word.split(',')
            words.extend(new_word)


    # Supprimer un symbole spécial entre les mots
    for word in words:
        for punctuation in punctuations:
            if punctuation in word:
                words.remove(word)
                new_word = word.split(punctuation)
                words.extend(new_word)

    # Supprimer le stopwords, les chaînes vides et les signes de ponctuation
    i = 0
    while i < len(words):
        if words[i].lower() in keywords or words[i] == '' or words[i] in punctuations or len(words[i]) == 1:
            words.remove(words[i])
            i -= 1
        i = i + 1

    return words

def frequency(file):
    # Statistical word frequency
    word_freq = {}
    words = index(file)
    for word in words:
        if word.lower() in word_freq:
            word_freq[word.lower()] += 1
        else:
            word_freq[word.lower()] = 1

    return word_freq
