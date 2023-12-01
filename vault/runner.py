import sys
import json
import argparse
from os import listdir, chdir, environ
from os.path import isfile, join, dirname, realpath
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

PATH = "vault/spiders/"

chdir(dirname(realpath(__file__)))

filenames = [f for f in listdir(PATH) if isfile(join(PATH, f))]
filenames = [f.replace('.py','') for f in filenames if not f.startswith("__")]

parser = argparse.ArgumentParser(prog='RUNNER')
parser.add_argument('-l', '--links', nargs='+', help='list of target websites (robots.txt links)')
parser.add_argument('-r', '--regex', nargs='+', help='list of url filters (well formed regex)')
args = parser.parse_args()

print("DEBUG: Crawlers", filenames, "PATH", PATH, "ARGS", args)

if not "ENV_LIST_WEBSITES" in environ:
    if args.links:
        environ['ENV_LIST_WEBSITES'] = json.dumps(args.links)
else:
    pass

process = CrawlerProcess(get_project_settings())

for fn in filenames:
    process.crawl(fn)

try:
    process.start()
except SystemExit:
    pass

sys.exit(0)