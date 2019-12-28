import os
import unicodedata

def gen_m3u(select_dir):
    if not os.path.isdir(select_dir):
        return

    def is_music(path):
        support_extension = ['.mp3', '.m3u', '.wma', '.flac',
            '.wav', '.mc', '.aac', '.m4a',
            '.ape', '.dsf', '.dff']
        _, extension = os.path.splitext(path)
        if extension.lower() in support_extension:
            return True
        return False

    def create_playList(select_dir):
        m3u_list = []
        for root, _, files in os.walk(select_dir):
            for filename in files:
                rel_dir = os.path.relpath(root, select_dir)
                if rel_dir == ".":
                    path = filename
                else:
                    path = os.path.join(rel_dir, filename)
                if is_music(path):
                    m3u_list.append(path)
        return m3u_list

    m3u_path = os.path.join(select_dir, os.path.basename(select_dir) + ".m3u8")

    if os.path.exists(m3u_path):
        os.remove(m3u_path)

    m3u_list = create_playList(select_dir)

    f = open(m3u_path, 'w', encoding='utf-8')
    for music in m3u_list:
        f.write(unicodedata.normalize('NFC', music) + '\n')
    f.close()

    return m3u_path