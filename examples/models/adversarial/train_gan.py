import tensorflow as tf

from nalp.corpus.text import TextCorpus
from nalp.datasets.language_modeling import LanguageModelingDataset
from nalp.encoders.integer import IntegerEncoder
from nalp.models.adversarial.gan import GAN

(train_images, train_labels), (_, _) = tf.keras.datasets.mnist.load_data()

train_images = train_images.reshape(train_images.shape[0], 28, 28, 1).astype('float32')
train_images = (train_images - 127.5) / 127.5 # Normalize the images to [-1, 1]

BUFFER_SIZE = 60000
BATCH_SIZE = 256

# Batch and shuffle the data
train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)

# # Creating a character TextCorpus from file
# corpus = TextCorpus(from_file='data/text/chapter1_harry.txt', type='char')

# # Creating an IntegerEncoder
# encoder = IntegerEncoder()

# # Learns the encoding based on the TextCorpus dictionary and reverse dictionary
# encoder.learn(corpus.vocab_index, corpus.index_vocab)

# # Applies the encoding on new data
# encoded_tokens = encoder.encode(corpus.tokens)

# # Creating Language Modeling Dataset
# dataset = LanguageModelingDataset(encoded_tokens, max_length=10, batch_size=64)

# Creating the GAN
gan = GAN()

#
# gan.D.build((64, 1, None))
# gan.G.build((64, 1, None))
# gan.build((64, 1, None))

# Compiling the GAN
gan.compile(optimizer=tf.optimizers.Adam(learning_rate=0.001),
            loss=tf.losses.BinaryCrossentropy(from_logits=True),
            metrics=[tf.metrics.SparseCategoricalAccuracy(name='accuracy')])

gan.fit(train_dataset, epochs=1)
