import os
import shutil
import unittest

import lib.m3u

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def create_three_fake_file(dir):
    touch(os.path.join(dir, 'mp3.mp3'))
    touch(os.path.join(dir, 'flac.flac'))
    touch(os.path.join(dir, 'docx.docx'))

class TestM3u(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._test_dir = '@test_temp_m3u_dir@'
        mutilple_level_dir = os.path.join(cls._test_dir, 'multiple_level')
        level_1_dir = os.path.join(mutilple_level_dir, 'level_1')
        single_level_dir = os.path.join(cls._test_dir, 'single_level')
        os.mkdir(cls._test_dir)
        os.makedirs(level_1_dir)
        os.makedirs(single_level_dir)
        create_three_fake_file(cls._test_dir)
        create_three_fake_file(mutilple_level_dir)
        create_three_fake_file(level_1_dir)
        create_three_fake_file(single_level_dir)
        cls._expect_result = [
            'flac.flac',
            'mp3.mp3',
            'multiple_level/flac.flac',
            'multiple_level/level_1/flac.flac',
            'multiple_level/level_1/mp3.mp3',
            'multiple_level/mp3.mp3',
            'single_level/flac.flac',
            'single_level/mp3.mp3'
        ]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._test_dir, ignore_errors=True)

    def test_is_music(self):
        self.assertTrue(lib.m3u.is_music("/i_am_mp3.mp3"))
        self.assertFalse(lib.m3u.is_music("/i_am_pptx.pptx"))

    def test_create_playList(self):
        actual_result = lib.m3u.create_playList(self._test_dir)
        self.assertEqual(self._expect_result, actual_result)

    def test_gen_m3u(self):
        m3u_path = '@test_temp_m3u_dir@/@test_temp_m3u_dir@.m3u8'
        self.assertEqual(m3u_path, lib.m3u.gen_m3u(self._test_dir))

        with open(m3u_path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        self.assertEqual(self._expect_result, content)

if __name__ == '__main__':
    unittest.main(verbosity=2)
