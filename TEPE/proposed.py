import random
import numpy as np

spl_char = ['#', '@', ',', '.', '?', '(', ')', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '/', '*', '=',
            '%']

# Define the Henon attractor
def henon_attractor(a, b, x0, y0, n):
    x, y = [x0], [y0]
    for _ in range(n - 1):
        x_next = 1 - a * x[-1] ** 2 + y[-1]
        y_next = b * x[-1]
        x.append(x_next)
        y.append(y_next)
    return x, y

# Define the logistic map
def logistic_map(r, x_init, n):
    values = [x_init]
    for _ in range(n - 1):
        x_next = r * values[-1] * (1 - values[-1])
        values.append(x_next)
    return values

# Initialize the matrix with unique values
def initialize_matrix(henon_x, henon_y, logistic_seq, size=7):
    matrix = np.empty((size, size), dtype='<U2')  # Adjusted for string storage
    counter = 0  # Counter for matrix indices

    # Combine alphabets and special characters into one list
    characters = [chr(65 + i) for i in range(26)] + ['#', '@', ',', '.', '?', '(', ')', '0', '1', '2', '3',
                                                      '4', '5', '6', '7', '8', '9', '+', '-', '/', '*', '=', '%']

    for i in range(len(henon_x)):
        x = counter // size  # taking the x-coordinate from the counter.
        y = counter % size  # taking the y-coordinate from the counter.
        char_index = int(float(logistic_seq[i]) * pow(10,7)) % len(characters)  # it's using the ASCII values.

        value = characters[char_index]
        characters.remove(value)  # Remove the used character from the list

        matrix[x, y] = value  # Overwrite existing value
        counter = (counter + 1) % (size * size)  # Increment counter and wrap around

    return matrix


# Utility functions for Playfair cipher
def format_text(text):
    # Remove non-letter characters and convert to uppercase
    text = ''.join(filter(str.isalpha, text.upper()))
    # Split text into digraphs, inserting 'X' if necessary
    text = [text[i:i+2] for i in range(0, len(text), 2)]
    for i, pair in enumerate(text):
        if len(pair) == 1:
            text[i] = pair + 'X'
        elif pair[0] == pair[1]:
            text[i] = pair[0] + 'X'
    return ''.join(text)

def encrypt_digraph(digraph, matrix):
    pos1 = np.argwhere(matrix == digraph[0])[0]
    pos2 = np.argwhere(matrix == digraph[1])[0]
    if pos1[0] == pos2[0]:
        # Same row, shift right
        encrypted_digraph = matrix[pos1[0], (pos1[1]+1) % 7] + matrix[pos2[0], (pos2[1]+1) % 7]
    elif pos1[1] == pos2[1]:
        # Same column, shift down
        encrypted_digraph = matrix[(pos1[0]+1) % 7, pos1[1]] + matrix[(pos2[0]+1) % 7, pos2[1]]
    else:
        # Rectangle, swap columns
        encrypted_digraph = matrix[pos1[0], pos2[1]] + matrix[pos2[0], pos1[1]]
    return encrypted_digraph

def decrypt_digraph(digraph, matrix):
    pos1 = np.argwhere(matrix == digraph[0])[0]
    pos2 = np.argwhere(matrix == digraph[1])[0]
    if pos1[0] == pos2[0]:
        # Same row, shift left
        decrypted_digraph = matrix[pos1[0], (pos1[1]-1) % 7] + matrix[pos2[0], (pos2[1]-1) % 7]
    elif pos1[1] == pos2[1]:
        # Same column, shift up
        decrypted_digraph = matrix[(pos1[0]-1) % 7, pos1[1]] + matrix[(pos2[0]-1) % 7, pos2[1]]
    else:
        # Rectangle, swap columns
        decrypted_digraph = matrix[pos1[0], pos2[1]] + matrix[pos2[0], pos1[1]]
    return decrypted_digraph

# Encrypt using the Playfair cipher
def playfair_encrypt(plaintext, matrix):
    formatted_text = format_text(plaintext)
    ciphertext = ''
    for i in range(0, len(formatted_text), 2):
        ciphertext += encrypt_digraph(formatted_text[i:i+2], matrix)
    return ciphertext

# Decrypt using the Playfair cipher
def playfair_decrypt(ciphertext, matrix):
    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        plaintext += decrypt_digraph(ciphertext[i:i+2], matrix)
    return plaintext

# Main program
def main():
    # Parameters for Henon attractor and logistic map
    a, b = 1.4, 0.3
    x0, y0 = 0.1, 0.1
    r, x_init = 3.99, 0.5
    n = 49  # Number of steps/values needed

    # Generate sequences
    henon_x, henon_y = henon_attractor(a, b, x0, y0, n)
    logistic_values = logistic_map(r, x_init, n)

    # Ensure both sequences have the same length
    min_len = min(len(henon_x), len(henon_y), len(logistic_values))
    henon_x = henon_x[:min_len]
    henon_y = henon_y[:min_len]
    logistic_values = logistic_values[:min_len]

    # Initialize the matrix with unique values
    matrix = initialize_matrix(henon_x, henon_y, logistic_values)  # Merging x and y for more values
    print(matrix)

    operation = input("Do you want to encrypt or decrypt the text? (e/d): ").lower().strip()
    text = input("Enter your text: ")

    if operation == 'e':
        encrypted_text = playfair_encrypt(text, matrix)
        print("Encrypted text:", encrypted_text)
    elif operation == 'd':
        decrypted_text = playfair_decrypt(text, matrix)
        print("Decrypted text:", decrypted_text)
    else:
        print("Invalid operation selected.")

if __name__ == "__main__":
    main()
