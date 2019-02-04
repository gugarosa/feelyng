import nalp.stream.loader as l
import nalp.stream.preprocess as p
from nalp.encoders.word2vec import Word2Vec

# Loads an input .csv
csv = l.load_csv('data/16k_twitter_en.csv')

# Creates a pre-processing pipeline
pipe = p.pipeline(
    p.lower_case,
    p.valid_char,
    p.tokenize_sentence
)

# Transforming dataframe into samples and labels
X = csv['text']
Y = csv['sentiment']

# Applying pre-processing pipeline to X
X = X.apply(lambda x: pipe(x))

# Creating a Word2Vec (Enconder's child) class
e = Word2Vec()

# Calling its internal method to learn an encoding representation
e.learn(X)

# Calling its internal method to actually encoded the desired data
# Does not necessarily needs to be the same X from e.learn()
e.encode(X)

# Acessing encoded data
print(e.encoded_data)
