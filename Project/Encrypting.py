import heapq, os, json

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if(other == None):
                return False
            if(not isinstance(other, HeapNode)):
                return False
            return self.freq == other.freq

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if(root == None):
            return
        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"
        keyfile_path = filename + "_key.txt"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output, open(keyfile_path, 'w') as keyfile:
            text = file.read()
            text = text.rstrip()
            
            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))

            json.dump(self.codes, keyfile) # write as JSON

        print("Encrypted file is at path : " + output_path)

    def get_code(self):
        return self.codes

    def get_reverse_mapping(self):
        return self.reverse_mapping


# Decryption
class HuffmanDecoding:
    def __init__(self, path, reverse_mapping, original_text):
        self.path = path
        self.reverse_mapping = reverse_mapping
        self.extended_text = original_text
        self.decoded_text = ""

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1*extra_padding]
        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                self.decoded_text += character
                current_code = ""
        return self.decoded_text

    def decompress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decrypted.txt"

        with open(self.path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while(len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        print("Decrypted file is at path : " + output_path)


def main():
    reverse_mapping = None  # declare reverse_mapping variable at the beginning

    user_choice = input("Enter 1 to encrypt a file or 2 to decrypt a file: ")

    if user_choice == '1':
        path = input("Enter the path of the file to be Encrypted: ")
        h = HuffmanCoding(path)
        h.compress()

        print("Encryption Key:")
        codes = h.get_code()
        for key in codes:
            print(key, ":", codes[key])

        # store the encryption key in a variable and give it to the user
        encryption_key = codes
        print("\nThe encryption key is:\n", encryption_key)

        # assign a value to reverse_mapping here
        reverse_mapping = h.get_reverse_mapping()

        print("\nThe reverse mapping is:\n", reverse_mapping)

    elif user_choice == '2':
        # reference reverse_mapping here
        path = input("Enter the path of the file to be decrypted: ")
        h = HuffmanDecoding(path, reverse_mapping, encryption_key)
        h.decompress()

    else:
        print("Wrong choice entered. Please enter 1 to encrypt a file or 2 to decrypt a file")
main()