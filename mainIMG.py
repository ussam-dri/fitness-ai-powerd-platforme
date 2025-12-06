
import json
import random
from io import BytesIO

import nltk
from nltk.corpus import stopwords
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import random

## RE-DOWNLOAD THESE TWO BEFORE THE FIRST RUN
#nltk.download('stopwords')
#nltk.download('punkt')
stop_words = set(stopwords.words('english'))
from IPython.display import Image

# Define the similarity threshold
SIMILARITY_THRESHOLD = 0.2

# Load the data from the JSON file
try:
    with open('imgitt.json') as f:
        data = json.load(f)
except FileNotFoundError:
    print("The file could not be found.")

# Extract the patterns, muscle tags, and response fields from the data
patterns = [pattern["patterns"] for pattern in data["intents"]]
muscles = [pattern["tag"] for pattern in data["intents"]]
response_fields = [pattern["responses"] for pattern in data["intents"]]

# Tokenize the patterns using NLTK
tokenized_patterns = []
for pattern_list in patterns:
    for pattern in pattern_list:
        tokens = nltk.word_tokenize(pattern)
        filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
        tokenized_patterns.append(filtered_tokens)

# Convert the response fields to a dictionary of muscle tag -> list of responses
muscle_responses = defaultdict(list)
for i in range(len(muscles)):
    muscle_responses[muscles[i]].extend(response_fields[i])

# Calculate the TF-IDF vectors for the patterns
pattern_documents = [' '.join(pattern_list) for pattern_list in patterns]
vectorizer = TfidfVectorizer()
pattern_vectors = vectorizer.fit_transform(pattern_documents)

from spellchecker import SpellChecker

spell = SpellChecker()

def generate_responseimg(user_input):

    # Tokenize the user input using NLTK
    tokens = nltk.word_tokenize(user_input)
    filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
    user_input_document = ' '.join(filtered_tokens)

    # Calculate the TF-IDF vector for the user input
    user_input_vector = vectorizer.transform([user_input_document])

    # Calculate the similarity between the user input and each pattern
    similarity_scores = cosine_similarity(user_input_vector, pattern_vectors)[0]

    # Find the index of the most similar pattern
    most_similar_index = similarity_scores.argmax()
    #print("inde:",most_similar_index)
    # Check if the most similar pattern meets the similarity threshold
    if similarity_scores[most_similar_index] < SIMILARITY_THRESHOLD:
        #img_url = "I'm sorry, I didn't understand that."
        #### casting img url
        img_url = 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjT2yYdSqGGIz51t1nZjX4Z1k88vNKLndCY1ePKstpvX7uoE4FB52k4Li1ZYAnoN6e1bpaZHJ0b_9WGCnEBoC-iBDbfEa0oahSpCcmTKLEc7j8CHxX0FbE4LO5hva5G0aDwifhe-BXBa-ygdWgE_ncp0An7n8kv4U9wZXMWqJsv80g6PhkIlgcr4T9aeQ/s1024/DALL·E%202023-04-01%2016.08.10%20-%20%20ai%20robot%20confused%20with%20an%20intergoation%20mak%20over%20his%20head%20.png'
    else:


        tag = muscles[most_similar_index]
        tag = spell.correction(tag)
        print("this is the tag",tag)
        if tag == "greeting":
            response = random.choice(response_fields[0])
            img_url = 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEid5p1X-4ZVJK7iN3s_2ucWzkERI1DtzelxUNC4ynefNK9NRWEAesUZfTHKecME1MmMoO31l73fcmc1M3NIjSIrRoH7vAOw_cCsjjjFC1LUONVzmSasfpxydhk-TypW6JYWK-A6i8XzjwWcAiX8F2ffNDCHjuhQ-d-Gks1fCgUylZ-WBwS1mpB21aYEXA/s320/DALL·E%202023-04-01%2016.09.09%20-%20%20ai%20robot%20confused%20with%20an%20saying%20hi%20.png'

        elif tag == "goodbye":

            img_url = 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgkuMtJK2fRGWiEeLtCK8KNSbCX4eT83icwU-3mpsWc1BVgP9PA2YmDdP1o0x5QtfZk5-CCEFeNZoZraX56hg9ekLN6ZPQyTN8s0fi9R6FZsdItBgIpIR-gwSTz3BehXv8DAdnvZrXLtTYJZJAezAlC2fE_1YstW86CgdXjgSuZ3P4Y0fPf8FuoxbVgtQ/s1024/DALL·E%202023-04-01%2016.13.21%20-%20%20ai%20robot%20confused%20with%20an%20saying%20bye%20gif.png'
            response = random.choice(response_fields[1])


        else:
            # Get the muscle tag for the most similar pattern
            muscle_tag = muscles[most_similar_index]
            # Get a random response for the muscle tag
            responses = muscle_responses[muscle_tag]
            response = random.choice(responses)
            ######### image part
            fitness_df = pd.read_csv('fitness_exercises.csv')
            img_urls = fitness_df[fitness_df['target'] == response]['gifUrl'].values
            # Show a random image
            img_url = random.choice(img_urls)
            response = "Here is an exercise you can try for your " + response + ":"

    #print("Bot:", response)
    #display(Image(url=img_url, width=200, height=200))

    return img_url





