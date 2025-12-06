import json
import random
import nltk
from nltk.stem import SnowballStemmer
from flask import Flask, request, render_template
from nltk.corpus import stopwords
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# nltk.download('punkt')
# nltk.download('stopwords')
#stemmer = SnowballStemmer("english")
stop_words = set(stopwords.words('english'))

SIMILARITY_THRESHOLD = 0.3

try:
    with open('texttt.json') as f:
        data = json.load(f)
except FileNotFoundError:
    print("The file could not be found.")

patterns = [pattern["patterns"] for pattern in data["intents"]]
muscles = [pattern["tag"] for pattern in data["intents"]]
response_fields = [pattern["responses"] for pattern in data["intents"]]

tokenized_patterns = []
for pattern_list in patterns:
    for pattern in pattern_list:
        tokens = nltk.word_tokenize(pattern)
        filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
        tokenized_patterns.append(filtered_tokens)

muscle_responses = defaultdict(list)
for i in range(len(muscles)):
    muscle_responses[muscles[i]].extend(response_fields[i])

pattern_documents = [' '.join(pattern_list) for pattern_list in patterns]
vectorizer = TfidfVectorizer()
pattern_vectors = vectorizer.fit_transform(pattern_documents)

from spellchecker import SpellChecker

spell = SpellChecker()



    # rest of the function code
# user_input = spell.correction(user_input)
# print("Start talking with the bot (type 'quit' to exit)")
def generate_response(user_input):

      while True:
        #user_input = input('You: ')
        if user_input == 'quit':
            break
        else:
                tokens = nltk.word_tokenize(user_input)
                filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
                user_input_document = ' '.join(filtered_tokens)

                user_input_vector = vectorizer.transform([user_input_document])
                similarity_scores = cosine_similarity(user_input_vector, pattern_vectors)[0]
                most_similar_index = similarity_scores.argmax()

                if similarity_scores[most_similar_index] < SIMILARITY_THRESHOLD:
                    response = "I'm sorry, I didn't understand that."
                else:
                    tag = muscles[most_similar_index]
                    if tag == "greeting":
                        response = random.choice(response_fields[0])
                    elif tag == "goodbye":
                        response = random.choice(response_fields[1])
                    else:
                        responses = muscle_responses[tag]
                        response = random.choice(responses)


                        fitness_df = pd.read_csv('output.csv')
                        fitness_df['BodyPart'] = fitness_df['BodyPart'].str.lower()
                        matching_rows = fitness_df.loc[fitness_df['BodyPart'] == response.lower()]

                        if matching_rows.empty:
                            print("No descriptions found for the specified body part.")
                        else:
                            random_row = matching_rows.sample(n=1)
                            response = "here is an exercies for your " + response + "\n" + random_row['Desc'].iloc[0]

                return response




