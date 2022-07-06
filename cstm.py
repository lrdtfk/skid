#!/usr/bin/env python3

# TODO: add io redirection
import argparse

class Custom:
    def __init__(self, word : str):
        self.__word = word.lower()
        self.__binary = ("0000", "0001", "0010", "0011", 
                         "0100", "0101", "0110", "0111", 
                         "1000", "1001", "1010", "1011", 
                         "1100", "1101", "1110", "1111")
        self.__table = self.table_generator()

        self.__LO_MASK = 0x000f
        self.__HI_MASK = 0x00f0
        self.__BITS_IN_NIBBLE = 4

    def table_generator(self):
        table = []

        for i in self.__binary:
            new_word = ''
            for j, k in zip(i, self.__word):
                if j == '1':
                    new_word += k.capitalize()
                else:
                    new_word += k
            table.append(new_word)
        return table

    def encode(self, src, dst):
        with open(src, 'r') as src_d:
            with open(dst, 'w') as dst_d:
                for line in src_d:
                    for char in line:
                        lo = (ord(char) & self.__LO_MASK)
                        hi = (ord(char) & self.__HI_MASK) >> \
                            self.__BITS_IN_NIBBLE
                        dst_d.write(self.__table[hi])
                        dst_d.write(self.__table[lo])

    def decode(self, src, dst):
        chunks = []
        with open(src, 'r') as src_d:
            with open(dst, 'w') as dst_d:
                for line in src_d:
                    for i in range(0, len(line), 4):
                        chunks.append(line[i:i+4])

                l = ''
                for i in range(0, len(chunks), 2):
                    hi_b = self.__table.index(chunks[i])
                    lo_b = self.__table.index(chunks[i+1])

                    res = (hi_b<<4) | (lo_b)
                    l += chr(res)

                dst_d.write(l)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=str,
                        help="word for encoding/decoding scheme")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encode", action="store_true",
                       help="encode data using *word*")
    group.add_argument("-d", "--decode", action="store_true",
                       help="decode data using *word*")
    parser.add_argument("-i", "--input-file", required=True,
                        help="specify a input data file")
    parser.add_argument("-o", "--output-file", required=True,
                        help="specify an output file")

    args = parser.parse_args()

    scm = Custom(args.word)
    if args.encode:
        scm.encode(args.input_file, args.output_file)
    elif args.decode:
        scm.decode(args.input_file, args.output_file)

