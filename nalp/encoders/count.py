import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

import nalp.utils.logging as l
from nalp.core.encoder import Encoder

logger = l.get_logger(__name__)


class CountEncoder(Encoder):
    """A CountEncoder class, responsible for learning a CountVectorizer encoding and
    further encoding new data.

    """

    def __init__(self):
        """Initizaliation method.

        """

        logger.info('Overriding class: Encoder -> CountEncoder.')

        # Overrides its parent class with any custom arguments if needed
        super(CountEncoder, self).__init__()

        logger.info('Class overrided.')

    def learn(self, tokens, top_tokens=100):
        """Learns a CountVectorizer representation based on the tokens' counting.

        Args:
            tokens (list): A list of tokens.
            top_tokens (int): Maximum number of top tokens to be learned.

        """

        logger.debug('Learning how to encode ...')

        # Creates a CountVectorizer object
        self.encoder = CountVectorizer(max_features=top_tokens,
                                       preprocessor=lambda p: p, tokenizer=lambda t: t)

        # Fits the tokens
        self.encoder.fit(tokens)

    def encode(self, tokens):
        """Encodes the data into a CountVectorizer representation.

        Args:
            tokens (list): A list of tokens to be encoded.

        Returns:
            A numpy array containing the encoded tokens.

        """

        logger.debug('Encoding new tokens ...')

        # Checks if enconder actually exists, if not raises an error
        if not self.encoder:
            # Creates the error
            e = 'You need to call learn() prior to encode() method.'

            # Logs the error
            logger.error(e)

            raise RuntimeError(e)

        # Applies the encoding to the new tokens
        encoded_tokens = (self.encoder.transform(tokens)).toarray()

        return encoded_tokens

    def decode(self, encoded_tokens):
        """Decodes the CountVectorizer representation back to tokens.

        Args:
            encoded_tokens (np.array): A numpy array containing the encoded tokens.

        Returns:
            A list of decoded tokens.

        """

        logger.debug('Decoding encoded tokens ...')

        # Checks if enconder actually exists, if not raises an error
        if not self.encoder:
            # Creates the error
            e = 'You need to call learn() prior to decode() method.'

            # Logs the error
            logger.error(e)

            raise RuntimeError(e)

        # Decoding the tokens
        decoded_tokens = self.encoder.inverse_transform(encoded_tokens)

        # Concatening the arrays output and transforming into a list
        decoded_tokens = (np.concatenate(decoded_tokens)).tolist()

        return decoded_tokens
