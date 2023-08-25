# Huffman-Encryption

heap is an empty list that will hold nodes representing characters and their frequencies
reverse_mapping is an empty dictionary that maps Huffman codes back to their corresponding characters, for decryption.

Heapnode:

The __init__ method creates an instance of the class which takes two parameters:
char, which should be a string representing the character associated with this node
freq, which should be an integer representing the frequency of the character
The other three methods, __lt__, __eq__, and __ne__, define how HeapNode objects can be compared to each other. 
Specifically, they allow us to use Python's built-in heapq module to create a heap where nodes are sorted by frequency.

Compress:

Parses the filename from self.path and modifies it to create a new filename with extension ".bin"
Opens the original file at self.path in read mode and the target compressed file in binary write mode
Reads the contents of the original file into a string variable text


Decompression: <br>
The decompress function takes the path of the compressed file as input, decompresses the data and writes it to a new file with _decrypted.txt appended to the original filename.
First, the function extracts the filename and extension from the input file path using os.path.splitext. It then creates an output file path by appending _deccrypted.txt to the filename.
The function opens both the input file in binary read mode and the output file in write mode. Inside a while loop, it reads each byte from the input file, converts it to a binary string of 8 bits using bin(byte)[2:].rjust(8, '0') and appends it to a bit_string variable. Once all bytes have been processed, the remove_padding function is called to remove the padding that was added during compression. The resulting encoded text is then passed to the decode_text function, which returns the original text that is written to the output file.
Finally, the function prints "Decrypted!" and returns the path of the output file.

The main function is the entry point of the program that prompts the user to choose between encrypting or decrypting a file.
Note: This implementation can only be used to decompress text data that has been compressed using Huffman coding implemented in this same class.
