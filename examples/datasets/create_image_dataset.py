import tensorflow as tf

from nalp.datasets.image import ImageDataset

# Loading the MNIST dataset
(x, y), (_, _) = tf.keras.datasets.mnist.load_data()

# Creating an Image Dataset
dataset = ImageDataset(x, batch_size=256, shape=(
    x.shape[0], 784), normalize=True)

# Iterating over one batch
for input_batch in dataset.batches.take(1):
    # For every input and target inside the batch
    for input in input_batch:
        # Transforms the tensor to numpy and print it
        print(input.numpy())