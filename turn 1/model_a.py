import unittest
import zlib
import io
import random


def compress(data):
    return zlib.compress(data)


def decompress(compressed_data):
    try:
        return zlib.decompress(compressed_data)
    except zlib.error as e:
        return None


class TestCompression(unittest.TestCase):

    def test_compression_decompression(self):
        data = b"This is some data to be compressed and decompressed."
        compressed_data = compress(data)
        decompressed_data = decompress(compressed_data)
        self.assertEqual(data, decompressed_data)

    def test_compression_ratio(self):
        data = b" " * 1024 * 1024  # 1MB of data
        compressed_data = compress(data)
        self.assertGreater(len(data), len(compressed_data))
        print(f"Compression ratio: {len(data) / len(compressed_data):.2f}")

    def test_decompression_error(self):
        corrupted_data = b"\x00" * 10
        decompressed_data = decompress(corrupted_data)
        self.assertIsNone(decompressed_data)


if __name__ == "__main__":
    unittest.main()
