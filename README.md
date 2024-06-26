This encoding or encryption method offers considerable complexity, which is positive for security. The combination of randomly generated keys each time, dictionary rotation, key addition in a specific order, and message masking provide multiple layers of protection against unauthorized decryption attempts, making it possible to decrypt only using this same program. 

For the program to function properly, it is recommended to place it in a folder of it's own. The encoded messages will be automatically exported to this folder. Likewise, to import a message for decoding, it must be added to the folder where the program resides, so that it can be recognized.

Below is a general overview of the encoding and decoding processes:

Encoding:

1)    Dictionary Preparation:
        * Five different dictionaries are generated from randomized lists of the alphabet and other characters. This process allows even uncoded messages that are exactly            the same to result in completely different codes after the encoding process.
        * Each dictionary is associated with a unique key, which is saved for use in the decoding process.

2)    Message Encoding:
       * The user enters the message to be encoded.
       * Each character of the message is encoded using the dictionaries in a rotating manner: the first character with the first dictionary, the second with the second                 dictionary, and so on. If the message is longer than the number of dictionaries, the process repeats from the first dictionary.

3)    Key Order Generation:
       * A list of five numbers, from 0 to 4, is generated, indicating the order in which the keys will be added to the message (e.g., 30421).

       * Each dictionary key is divided into two parts. The first parts of the keys are inserted at the beginning of the encoded message in the order specified by the               previously generated list, and the second parts of the keys are inserted at the end of the message. Finally, the key order is inserted at the beginning of the message.

4)    Message Masking:
        * A percentage of the total of characters at that point is added to the encoded message to mask the real encoded message, and to make its analysis more difficult.

5)    The encoded message is exported to a txt file to be sent to the recipient.

Decoding:

1)   Unmasking:
       * The characters added to mask the original message are removed.

2)   Key Extraction and Application:
       * The list of five numbers at the beginning of the message is used to determine the order of the keys.
       * The parts of the keys are extracted in the corresponding order and the five keys are reassembled.
       * The keys are used to restore the dictionaries used to encode the message being processed.

3)    Message Decoding:
       * With the dictionaries restored, the original message is decoded using the dictionaries in the same rotating order used during encoding, but with the key-value pairs            inverted.

4)   The decoded message is displayed on the console.

To personalize this app and make it unique for your purposes, you could make, for example, some of the following changes, or all of them:

* Use a different quantity of dictionaries (Be carefull to update the key ordering list and related code too, if you do this).
* Use different characteres for the masking process.
* Change the order of elements of the "base tuple" (abc_tupla), which is essential, as it is the only common ground between all the random stuff.
