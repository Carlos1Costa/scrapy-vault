import os
import string
import scrapy
from scrapy.http import FormRequest
from urllib.parse import urlparse, parse_qs
from pathlib import Path


class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["vimm.net"]
    start_urls = [
                    #"https://vimm.net/vault/Atari2600", 
                    #"https://vimm.net/vault/NES",
                    "https://vimm.net/vault/SMS", # Master System
                    #"https://vimm.net/vault/Genesis", # Mega Drive
                    #"https://vimm.net/vault/SNES",
                    #"https://vimm.net/vault/N64",
                    #"https://vimm.net/vault/GB",
                    #"https://vimm.net/vault/Lynx",
                    #"https://vimm.net/vault/GG",
                    #"https://vimm.net/vault/GBC",
                    #"https://vimm.net/vault/GBA"
                  ]

    def _parse_url_param(self, url, parameter):
        parsed_url = urlparse(url)
        captured_value = parse_qs(parsed_url.query)[parameter][0]
        return captured_value

    def _parse_domain(self, response):
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

        cartridge_xpath = '//table[contains(@class, "hovertable")]//td/a[not(contains(@href, "p=rating")) and contains(@href, "/vault/")]//@href'
        cartridge_urls = response.xpath(cartridge_xpath)

        for url in cartridge_urls:
            full_domain_url = self._parse_domain(response) + url.extract()
            self.logger.info("parse(), full_domain_url: %s", full_domain_url)
            yield scrapy.Request(url=full_domain_url, callback=self.parse_cartridge, meta={'console_name': console_name})

    def parse_cartridge(self, response):        
        good_title = ''.join(response.xpath('//span[@id="data-good-title"]/text()').extract()).strip()
        
        form_data = {
            "mediaId": response.xpath('//form[@id="download_form"]/input[@name="mediaId"]/@value').extract()[0],
            "alt": "0",
            'good_file': Path(good_title).stem + ".zip",
            'console_name': response.meta['console_name']
        }
        yield FormRequest.from_response(response, formid='download_form', method="GET",
                                        formdata=form_data, callback=self.parse_download)
        
    def parse_download(self, response):
        folder = "./ROMS/" + self._parse_url_param(response.url, 'console_name') + "/"
        file_name = folder + self._parse_url_param(response.url, 'good_file')
        self.logger.info("parse_dowload(), saving file: '%s' '%s'", len(response.body), file_name)
        os.makedirs(folder,  exist_ok=True)
        with open(file_name, 'wb') as f:
            f.write(response.body)