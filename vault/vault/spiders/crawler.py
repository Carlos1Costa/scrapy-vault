import string
import scrapy
from urllib.parse import urlparse


class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["vimm.net"]
    start_urls = [
                    #"https://vimm.net/vault/Atari2600", 
                    #"https://vimm.net/vault/NES",
                    #"https://vimm.net/vault/SMS", # Master System
                    #"https://vimm.net/vault/Genesis", # Mega Drive
                    #"https://vimm.net/vault/SNES",
                    #"https://vimm.net/vault/N64",
                    #"https://vimm.net/vault/GB",
                    "https://vimm.net/vault/Lynx",
                    #"https://vimm.net/vault/GG",
                    #"https://vimm.net/vault/GBC",
                    #"https://vimm.net/vault/GBA"
                  ]

    def parse_domain(self, response):
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return domain

    def start_requests(self):
        for url in self.start_urls:
            console_name = url.split('/vault/')[1] ## this is not a good way to solve it :P
            self.logger.info("start_requests(), console_name: %s", console_name)

            vault_console = [url + '/' + j for j in string.ascii_uppercase]
            for index_page in vault_console:
                self.logger.info("start_requests(), index_page: %s", index_page)
                yield scrapy.Request(url=index_page, callback=self.parse, meta={'console_name': console_name})
    
    def parse(self, response):
        console_name = response.meta['console_name']
        self.logger.info("parse(), console_name: %s", console_name)

        cartridge_xpath = '//table[contains(@class, "hovertable")]//td/a/@href'
        cartridge_urls = response.xpath(cartridge_xpath)

        for url in cartridge_urls:
            full_domain_url = self.parse_domain(response) + url.extract()
            self.logger.info("parse(), ull_domain_url: %s", full_domain_url)
            yield scrapy.Request(url=full_domain_url, callback=self.parse_cartridge, meta={'console_name': console_name})

    def parse_cartridge(self, response):
        self.logger.info("parse_cartridge(), response.url: %s", response.url)
        console_name = response.meta['console_name']
        self.logger.info("parse_cartridge(), console_name: %s", console_name)

        good_title = ''.join(response.xpath('//span[@id="data-good-title"]/text()').extract()).strip()
        self.logger.info("parse_cartridge(), good_title: '%s'", good_title)

        img_src = ''.join(response.xpath('//a[contains(@onclick, "libretro")]/img/@src').extract()).strip()
        img_src = self.parse_domain(response) + img_src
        self.logger.info("parse_cartridge(), img_src: '%s'", img_src)

        download_file = response.xpath('//form[@id="download_form"]')
        self.logger.info("parse_cartridge(), download_file: '%s'", download_file)
