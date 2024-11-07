import requests
from collections import Counter
import random as rnd

#---Code reçu devoir
def cut_string_into_pairs(text):
  pairs = []
  for i in range(0, len(text) - 1, 2):
    pairs.append(text[i:i + 2])
  if len(text) % 2 != 0:
    pairs.append(text[-1] + '_')  # Add a placeholder if the string has an odd number of characters
  return pairs

def load_text_from_web(url):
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"An error occurred while loading the text: {e}")
    return None
  
url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
corpus = load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
corpus = corpus + load_text_from_web(url)


url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
text = load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
text = text + load_text_from_web(url)

caracteres = list(set(list(text)))
nb_caracteres = len(caracteres)
nb_bicaracteres = 256-nb_caracteres
bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(text)).most_common(nb_bicaracteres)]
symboles = caracteres + bicaracteres
nb_symboles = len(symboles)

def gen_key(symboles):

  l=len(symboles)
  if l > 256:
    return False

  rnd.seed(1337)
  int_keys = rnd.sample(list(range(l)),l)
  dictionary = dict({})
  for s,k in zip(symboles,int_keys):
    dictionary[s]="{:08b}".format(k )
  return dictionary

dictionaire = gen_key(symboles)

def M_vers_symboles(M, K):
    encoded_text = []
    i = 0

    while i < len(M):
        # Vérifie les paires de caractères
        if i + 1 < len(M):
            pair = M[i] + M[i + 1]
            if pair in dictionaire:
                encoded_text.append(pair)
                i += 2  # Sauter les deux caractères utilisés
                continue

        # Vérifie le caractère seul
        if M[i] in K:
            encoded_text.append(M[i])
        else:
            # Conserve le caractère tel quel si non trouvé
            encoded_text.append(M[i])
        i += 1

    return encoded_text
#---Fin code reçu


def decrypt(C):
  #Générer les symboles
  url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
  text = load_text_from_web(url)
  url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
  text = text + load_text_from_web(url)

  caracteres = list(set(list(text)))
  nb_caracteres = len(caracteres)
  nb_bicaracteres = 256-nb_caracteres
  bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(text)).most_common(nb_bicaracteres)]
  symboles = caracteres + bicaracteres
  nb_symboles = len(symboles)

  #Analyse de fréquences dans des texts en français
  url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  
  texteAnalyse = text + load_text_from_web(url)
  symbolesLangueFR = M_vers_symboles(texteAnalyse,symboles)
  
  compteurSymbolesLangueFR = Counter(symbolesLangueFR)
  symbolesCommunsFR = compteurSymbolesLangueFR.most_common()
  
  #Séparer le cryptogramme en séquences
  # Séparer C en blocs de 8 bits
  C_Sequence8bits = [C[i:i+8] for i in range(0, len(C), 8)]
    
  # Compter la fréquence des blocs dans le texte chiffré
  compteurSymbolesC = Counter(C_Sequence8bits)
  sequencesCommunesC = compteurSymbolesC.most_common()
  # Associer les symboles les plus fréquents avec les sequences les plus fréquentes
  correspondances = {}
  for (sequence, _), (symbole, _) in zip(sequencesCommunesC, symbolesCommunsFR):
        correspondances[sequence] = symbole

  #Déchiffrement en remplaçant les sequences par les symboles associés
  texteDechiffre = []
  for bloc in C_Sequence8bits:
      if bloc in correspondances:
          texteDechiffre.append(correspondances[bloc])
      else:
          texteDechiffre.append('?')  # Pour les blocs non trouvés
  
  M = ''.join(texteDechiffre)
  return M