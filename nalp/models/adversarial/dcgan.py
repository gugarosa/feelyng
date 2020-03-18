import math

import tensorflow as tf
from tensorflow.keras import layers

import nalp.utils.logging as l
from nalp.models.base import AdversarialModel, Model

logger = l.get_logger(__name__)


class Discriminator(Model):
    """A Discriminator class stands for the discriminative part of a Deep Convolutional Generative Adversarial Network.

    """

    def __init__(self, alpha=0.3, dropout=0.3):
        """Initialization method.

        Args:
            alpha (float): LeakyReLU activation threshold.
            dropout (float): Dropout activation rate.

        """

        logger.info('Overriding class: Model -> Discriminator.')

        # Overrides its parent class with any custom arguments if needed
        super(Discriminator, self).__init__(name='D_dcgan')

        # Defining an alpha property for the LeakyReLU activation
        self.alpha = alpha

        # Defining a dropout rate property for the Dropout layer
        self.dropout_rate = dropout

        # Defining the first convolutional layer
        self.conv1 = layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same')

        # Defining the first dropout layer
        self.drop1 = layers.Dropout(dropout)

        # Defining the second convolutional layer
        self.conv2 = layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same')

        # Defining the second dropout layer
        self.drop2 = layers.Dropout(dropout)

        # Defining the output as a logit unit that decides whether input is real or fake
        self.out = layers.Dense(1)

    def call(self, x, training=True):
        """Method that holds vital information whenever this class is called.

        Args:
            x (tf.Tensor): A tensorflow's tensor holding input data.
            training (bool): Whether architecture is under training or not.

        Returns:
            The same tensor after passing through each defined layer.

        """

        # Passing down first convolutional layer with LeakyReLU activation and Dropout
        x = self.drop1(tf.nn.leaky_relu(
            self.conv1(x), self.alpha), training=training)

        # Passing down second convolutional layer with LeakyReLU activation and Dropout
        x = self.drop2(tf.nn.leaky_relu(
            self.conv2(x), self.alpha), training=training)

        # Passing down the output layer
        x = self.out(x)

        return x


class Generator(Model):
    """A Generator class stands for the generative part of a Generative Adversarial Network.

    """

    def __init__(self, n_input=100, n_output=784, alpha=0.3):
        """Initialization method.

        Args:
            n_input (int): Number of input (noise) dimension.
            n_output (int): Number of output units.
            alpha (float): LeakyReLU activation threshold.

        """

        logger.info('Overriding class: Model -> Generator.')

        # Overrides its parent class with any custom arguments if needed
        super(Generator, self).__init__(name='G_dcgan')

        # Defining an alpha property for the LeakyReLU activation
        self.alpha = alpha

        # Defining a property for the input noise dimension
        self.n_input = n_input

        # Based on the number of output features, we calculate the number of initial strides
        initial_strides = int(math.sqrt(n_output) / 4)

        # Defining the first linear layer
        self.linear1 = layers.Dense(initial_strides ** 2 * 256, use_bias=False)

        # Defining the first batch normalization layer
        self.bn1 = layers.BatchNormalization()

        # Defining the first convolutional transpose layer
        self.conv1 = layers.Conv2DTranspose(
            128, (5, 5), strides=(1, 1), padding='same', use_bias=False)

        # Defining the second batch normalization layer
        self.bn2 = layers.BatchNormalization()

        # Defining the second convolutional transpose layer
        self.conv2 = layers.Conv2DTranspose(
            64, (5, 5), strides=(2, 2), padding='same', use_bias=False)

        # Defining the third batch normalization layer
        self.bn3 = layers.BatchNormalization()

        # Defining the third convolutional transpose layer
        self.conv3 = layers.Conv2DTranspose(1, (5, 5), strides=(
            2, 2), padding='same', use_bias=False, activation='tanh')


    def call(self, x, training=True):
        """Method that holds vital information whenever this class is called.

        Args:
            x (tf.Tensor): A tensorflow's tensor holding input data.
            training (bool): Whether architecture is under training or not.

        Returns:
            The same tensor after passing through each defined layer.

        """

        # Passing down first convolutional transpose layer with Batch Normalization and LeakyReLU activation
        x = tf.nn.leaky_relu(
            self.bn1(self.linear1(x), training=training), self.alpha)

        x = tf.reshape(x, (x.shape[0], 7, 7, 256))

        # Passing down first convolutional transpose layer with Batch Normalization and LeakyReLU activation
        x = tf.nn.leaky_relu(
            self.bn2(self.conv1(x), training=training), self.alpha)

        # Passing down second convolutional transpose layer with Batch Normalization and LeakyReLU activation
        x = tf.nn.leaky_relu(
            self.bn3(self.conv2(x), training=training), self.alpha)

        # Passing down third convolutional transpose layer with Batch Normalization and LeakyReLU activation
        x = self.conv3(x)

        return x


class DCGAN(AdversarialModel):
    """A DCGAN class is the one in charge of Deep Convolutional Generative Adversarial Networks implementation.

    References:
        A. Radford, L. Metz, S. Chintala. Unsupervised representation learning with deep convolutional generative adversarial networks. Preprint arXiv:1511.06434 (2015).

    """

    def __init__(self, gen_input=100, gen_output=784, alpha=0.3, dropout=0.3):
        """Initialization method.

        Args:
            gen_input (int): Number of input (noise) dimension in the Generator.
            gen_output (int): Number of output units in the Generator.
            alpha (float): LeakyReLU activation threshold.
            dropout (float): Dropout activation rate.

        """

        logger.info('Overriding class: AdversarialModel -> DCGAN.')

        # Creating the discriminator network
        D = Discriminator(alpha=alpha, dropout=dropout)

        # Creating the generator network
        G = Generator(n_input=gen_input, n_output=gen_output, alpha=alpha)

        # Overrides its parent class with any custom arguments if needed
        super(DCGAN, self).__init__(D, G, name='dcgan')