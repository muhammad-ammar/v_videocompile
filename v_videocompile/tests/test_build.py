
import os
import sys
import unittest

"""
build test

"""
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))
    )
from v_videocompile import VideoCompile


class BuildTest(unittest.TestCase):
    """
    Simple build test -- checks 'check'
    
    """
    def setUp(self):
        self.V = VideoCompile()
        self.x = os.system('ffmpeg')

    def test_defaults(self):
        if self.x > 0:
            self.assertFalse(self.V.check())
            return None
        self.assertTrue(self.V.check())


def main():
    unittest.main()


if __name__ == '__main__':
    sys.exit(main())

