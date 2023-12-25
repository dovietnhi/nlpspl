import pandas as pd
from gensim.models import Word2Vec
from pyvi import ViTokenizer

# Load the Word2Vec model
model_path = 'word2vec_model.bin'
w2v_model = Word2Vec.load(model_path).wv

# Function to correct spelling
def correct_spelling(word):
    if word not in w2v_model.key_to_index:
        # If the word is not in the vocabulary, return the original word
        return word
    
    # If the word is in the vocabulary, return the most similar word
    similar_words = w2v_model.most_similar(word)
    return similar_words[0][0]

# Read data from the CSV file
input_file = 'input.csv'
df = pd.read_csv(input_file)

# Apply the spelling correction function to each column in the dataframe
for column in df.columns:
    df[column] = df[column].apply(lambda x: ' '.join([correct_spelling(word) for word in ViTokenizer.tokenize(x).split()]))

# Save the corrected dataframe to a new CSV file
output_file = 'output.csv'
df.to_csv(output_file, index=False)
