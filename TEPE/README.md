# TEPE: The Enigmatic Playfair Encryption

This repository contains Python implementations of the Playfair Cipher encryption and decryption methods, including the proposed method by Assia Merzoug et al. and an improved version that incorporates dynamic keying and chaos theory principles.

## Proposed Method

The proposed method by Assia Merzoug et al. introduces the use of chaos theory, specifically the Hénon attractor and the logistic map, to generate a unique key matrix for the Playfair Cipher. The key matrix is initialized with unique values derived from the chaotic sequences.

### Improved Method

The improved method builds upon the proposed method by incorporating dynamic keying and a shuffling matrix approach. After encrypting each character, the key matrix is rotated based on a predefined step value, introducing an additional layer of security and complexity. The step value is embedded within the ciphertext, making it resistant to frequency analysis attacks.

#### Usage

To use the proposed method, you can run the following Python script: TEPE.py[TEPE.py]


#####Requirements

This project requires Python 3.x and the following libraries:
  NumPy

You can install the required libraries using pip:

```pip install numpy```

#######Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.



