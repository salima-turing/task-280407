import unittest
import zlib
from io import BytesIO
from random import random


# Function to compress data
def compress_data(data):
    compressed_data = zlib.compress(data)
    return compressed_data


# Function to decompress data
def decompress_data(compressed_data):
    return zlib.decompress(compressed_data)


# We will use this function to simulate network transmission
def send_data_over_network(data, chunk_size=None, packet_loss_probability=0):
    """
    Simulates sending data over the network.
    - If chunk_size is None, it sends the data in one go.
    - Otherwise, it sends data in chunks of chunk_size bytes.
    """
    if chunk_size is None:
        return data

    output = BytesIO()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]

        # Simulate packet loss
        if random() < packet_loss_probability:
            print(f"Simulating packet loss for chunk {i // chunk_size + 1}")
            continue  # Skip sending this chunk (simulate packet loss)

        # Simulate network transmission delay (optional)
        # time.sleep(0.001)
        output.write(chunk)
    return output.getvalue()


class TestDataCompression(unittest.TestCase):

    def test_compress_decompress_over_network(self):
        # Data to be compressed
        original_data = b"Lorem ipsum dolor sit amet"

        # Compress the data
        compressed_data = compress_data(original_data)

        # Simulate network transmission with a small chunk size to simulate limitations
        chunk_size = 4  # For demonstration purposes
        transmitted_data = send_data_over_network(compressed_data, chunk_size)

        # Now, let's test the decompression process
        with self.subTest("Decompression with limited transmission"):
            decompressed_data = decompress_data(transmitted_data)
            # Verify that the decompressed data is the same as the original
            self.assertEqual(original_data, decompressed_data)

    def test_compress_decompress_with_packet_loss(self):
        original_data = b"Lorem ipsum dolor sit amet"
        compressed_data = compress_data(original_data)

        # Simulate network transmission with packet loss
        chunk_size = 4
        packet_loss_probability = 0.2  # Probability of losing a packet
        transmitted_data = send_data_over_network(compressed_data, chunk_size, packet_loss_probability)

        with self.subTest("Decompression with packet loss"):
            # Decompression may raise an error if packet loss occurred
            with self.assertRaises(zlib.error):
                decompress_data(transmitted_data)

if __name__ == "__main__":
    unittest.main()
