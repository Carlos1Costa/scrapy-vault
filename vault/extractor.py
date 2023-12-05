'''
walk a file tree from specified starting point, unzip any zip files encountered in the
directory where zip file was found, and then delete the zip file after succesfully
unzipping
'''

import os
import re
import zipfile
import hashlib
import logging


folder_root = './vault/ROMS'
suffix = ".zip"
checksum_file = "Vimm's Lair.txt"
extractor_log = "extractor.log"


def setup_logger():
    os.remove(extractor_log)
    logging.basicConfig(filename=extractor_log, level=logging.INFO)

def md5_grab(txtfile):
    match = re.search(r"(?<=MD5:\s{3})\w{32}", txtfile)
    if match:
        md5_value = match.group()
        return md5_value
    else:
        logging.info("ERROR NO MD5")
        return None
    
def checksum(md5_value, current_rom):
    try:
        tmp = hashlib.md5(open(current_rom,'rb').read()).hexdigest()
        if tmp == md5_value:
            logging.info("MD5 MATCH")
        else:
            logging.info("ERROR MD5 DID NOT MATCH")
    except Exception as ex:
        logging.info(ex)

def main():
    for folder, dirs, files in os.walk(folder_root, topdown=False):
        for name in files:
            if name.endswith(suffix):
                try:
                    zip_file = zipfile.ZipFile(os.path.join(folder, name))
                except Exception as ex:
                    logging.info(ex)
                    continue

                rom_name = [f for f in zip_file.namelist() if f != checksum_file][0]
                logging.info("FOLDER='{0}', ZIP_FILE_NAME='{1}', ROM_NAME='{2}'".format(folder, name, rom_name))

                text = None
                try:
                    text = zip_file.read(checksum_file).decode(encoding="utf-8")
                    text = md5_grab(text)
                except:
                    logging.info("ERROR NO FILE")
                
                zip_file.extractall(path=folder)

                if text:
                    logging.info("ROM='{0}', CURRENT MD5='{1}'".format(rom_name, text))
                    checksum(text, os.path.join(folder, rom_name))

                zip_file.close()
                try:
                    os.remove(os.path.join(folder, checksum_file))
                except:
                    logging.info("ERROR NO CHECKSUM")
                os.remove(os.path.join(folder, name))


if __name__ == '__main__':
    setup_logger()
    main()