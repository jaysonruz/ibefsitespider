from scrapy.spiders import SitemapSpider
import os

class DownloadlinkSpider(SitemapSpider):
    '''
    crawls through sitemap and downloads pdf from links that contain '-presentation',
    '''

    name = 'downloadlink'
    allowed_domains = ['www.ibef.org']
    sitemap_urls = ['https://www.ibef.org/sitemap.xml']

    sitemap_rules =  [('-presentation', 'parse_article')]
    
    def parse_article(self, response):
        
        
        link=response.xpath("//img[@alt='Download PDF']/parent::node()/@name").extract() #type of elem is a --> list of 1 url
        if ".pdf" in str(link):
            yield response.follow(link[0], self.save_file,meta={'link':link})

    def save_file(self, response):
        link=response.meta['link']
        save_path = os.getcwd()+"\\pdfs"
        filename = response.url.split("/")[-1] # assume the last path of url is the name
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        completeName = os.path.join(save_path, filename)

        with open(completeName, 'wb') as f: # open a new file
            f.write(response.body)      # write content downloaded
        self.logger.info('Save file %s', filename) # display the file downloaded
        
        yield {"url":link}