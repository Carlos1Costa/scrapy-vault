
import sys
from os import listdir, chdir
from os.path import isfile, join, dirname, realpath
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

PATH = "vault/spiders/"

chdir(dirname(realpath(__file__)))

filenames = [f for f in listdir(PATH) if isfile(join(PATH, f))]
filenames = [f.replace('.py','') for f in filenames if not f.startswith("__")]

process = CrawlerProcess(get_project_settings())

for fn in filenames:
    process.crawl(fn)

try:
    process.start()
except SystemExit:
    pass

sys.exit(0)