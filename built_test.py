
import os
import sys

"""

pip test

"""

from ffmpeg_compiler import FFCompiler


def test():

    F = FFCompiler()
    F.run()

if __name__ == '__main__':
    test()
