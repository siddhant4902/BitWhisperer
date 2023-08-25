# Huffman-Encryption

Huffman coding:

path is a string that represents the path to a file that will be compressed
heap is an empty list that will hold nodes representing characters and their frequencies
codes is an empty dictionary that will store Huffman codes for each character in the input file
reverse_mapping is an empty dictionary that maps Huffman codes back to their corresponding characters.

Heapnode:

The __init__ method creates an instance of the class which takes two parameters:
char, which should be a string representing the character associated with this node
freq, which should be an integer representing the frequency of the character
The other three methods, __lt__, __eq__, and __ne__, define how HeapNode objects can be compared to each other. 
Specifically, they allow us to use Python's built-in heapq module to create a heap where nodes are sorted by frequency.


Methods:

The make_frequency_dict method takes in a string text and creates a dictionary frequency where each key is a character from text, and the corresponding value is the count of that character in text. For example, if text is "abacabadabacaba", frequency would be {'a': 8, 'b': 4, 'c': 2, 'd': 2}. This dictionary is then returned.
The make_heap method takes in the frequency dictionary and uses it to create a heap of HeapNode objects based on the frequency of their associated characters. It does so by iterating through the keys of frequency, creating a HeapNode object for each key-value pair, and pushing that node onto the heap using heapq.heappush(). The heap will now be sorted by increasing frequency of characters.
The merge_nodes method takes the two smallest nodes from the heap, combines them into a new node with a null character and a frequency equal to the sum of the frequencies of the two nodes. The left and right pointers of this new node are set to the two nodes which were combined. This new node is then pushed back onto the heap with heapq.heappush(). The process is repeated until there is only one node left on the heap, which represents the root of the Huffman tree.
The make_codes_helper method performs a depth-first traversal of the Huffman tree to assign a binary code to each leaf node (i.e. character), starting from the root. Each time the method is called recursively with the left child of a node, it appends a 0 to the current code; when called with the right child, it appends a 1. If it reaches a leaf node, it stores both the current code and its corresponding character in self.codes and self.reverse_mapping, respectively.
The make_codes method first pops the root node from the heap (which should be the only node remaining after merge_nodes() has been called). It then calls make_codes_helper on the root node to create binary codes for each character.
The get_encoded_text method takes in a string text, which presumably represents the input text file. It iterates through each character in text, retrieves its corresponding binary code from self.codes, and concatenates all the binary codes together into a single string encoded_text, which is returned.
The pad_encoded_text method pads the binary encoded text so that it can be divided into bytes (8-bit chunks) and stored as an integer. It calculates the number of extra padding bits required to make the length of encoded_text a multiple of 8, and adds them to the end of encoded_text. It then converts the number of padding bits to an 8-bit binary string and concatenates it to the beginning of encoded_text. The padded and encoded text is returned.
The get_byte_array method takes in the padded binary encoded text as a string padded_encoded_text, checks that its length is a multiple of 8, and converts it into a bytearray b by iterating over every 8 bits and converting them into integers. This bytearray can then be written to a binary file.

Compress:

Parses the filename from self.path and modifies it to create a new filename with extension ".bin"
Opens the original file at self.path in read mode and the target compressed file in binary write mode
Reads the contents of the original file into a string variable text
Calls make_frequency_dict, make_heap, merge_nodes, make_codes, get_encoded_text, pad_encoded_text, and get_byte_array to compress the input text and get a bytearray for output.
Writes the bytearray to the output file
Closes both files and prints a message indicating success
It returns the name of the compressed file as a string output_path.


Decompression:
The remove_padding function takes in the padded encoded text and returns the original encoded text by removing the padding.
The first 8 bits of the padded encoded text represent the number of extra padded zeroes added to the end of the original encoded text so that it can be evenly divided into bytes (each byte represents 8 bits). The function extracts this information and converts it back to an integer using int(padded_info, 2) where 2 represents the binary number system.
Next, the function removes the first 8 bits from the padded encoded text and then removes the last extra_padding number of bits from the end of the encoded text to get the original encoded text.
The decode_text function takes in the encoded text and uses the Huffman tree's reverse mapping (which maps codes to characters) to decode the original text.
It iterates through each bit of the encoded text and appends each bit to the current_code string. When current_code matches a valid code in the reverse mapping, the corresponding character is appended to the decoded_text string and current_code is reset. The loop continues until all bits in the encoded text have been processed and the entire decoded text has been reconstructed.
The decompress function takes the path of the compressed file as input, decompresses the data and writes it to a new file with _decrypted.txt appended to the original filename.
First, the function extracts the filename and extension from the input file path using os.path.splitext. It then creates an output file path by appending _deccrypted.txt to the filename.
The function opens both the input file in binary read mode and the output file in write mode. Inside a while loop, it reads each byte from the input file, converts it to a binary string of 8 bits using bin(byte)[2:].rjust(8, '0') and appends it to a bit_string variable. Once all bytes have been processed, the remove_padding function is called to remove the padding that was added during compression. The resulting encoded text is then passed to the decode_text function, which returns the original text that is written to the output file.
Finally, the function prints "Decrypted!" and returns the path of the output file.
The main function is the entry point of the program that prompts the user to choose between encrypting or decrypting a file.
If the user chooses to encrypt a file, the function takes the path of the original file and creates an instance of the HuffmanCoding class with this path. It then calls the compress function on this instance to compress the text data in the input file. The encrypted output is written to a new file and the encryption key is saved in a separate file called key.txt.
If the user chooses to decrypt a file, the function prompts the user to provide both the paths of the encrypted file and the file containing the encryption key. It reads the encryption key from the key file and stores it in a dictionary. The HuffmanCoding class is instantiated with the encrypted file's path, and codes attribute of this instance is set to the dictionary containing the encryption key. Finally, the decompress function is called to write the decrypted text to a new file.
If the user enters an invalid choice, an appropriate message is displayed.

Note: This implementation can only be used to decompress text data that has been compressed using Huffman coding implemented in this same class.
