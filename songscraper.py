from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
import goose3
import csv

g = goose3.Goose()

song_prefix = "Lyrics and music to all your favorite Christmas songs and Christmas carols"

class ChristmasSpider(CrawlSpider):
    custom_settings = {
							"RETRY_TIMES":3,
							"CONCURRENT_REQUESTS": 10,
							"SCHEDULER_DISK_QUEUE":'scrapy.squeue.PickleFifoDiskQueue',
							"SCHEDULER_MEMORY_QUEUE":'scrapy.squeue.FifoMemoryQueue',
							"DEPTH_LIMIT": 6,
							"TELNETCONSOLE_PORT": None,
							}   
    def __init__(self):
        self.name = "christmascrawler"
        self.allowed_domains = ["http://www.christmas-songs.org",
            "www.christmas-songs.org",
            "christmas-songs.org"]
        self.start_urls = ["http://www.christmas-songs.org"]
        self._rules = [
            Rule(LinkExtractor(allow=(),),
			callback=self.parse_item, follow=True)
        ]
        self.writer = csv.writer(open("songs.csv", "w"))
	
    def parse_start_url(self, response):
        yield self.parse_item(response)	

    def parse_item(self, response):
        url = response.url
        
        def clean_song(url, html):
            raw_song = g.extract(raw_html=str(response.body)).cleaned_text
            cleaned_song1 = raw_song.replace("\n",
                " ").replace("\\r", "").replace("\\", "")
            cleaned_song2 = cleaned_song1.replace(song_prefix, "")
            name = url.split("/songs/")[1].replace("_", " ").replace(".html", "")
            return name, cleaned_song2
            
        if "/songs/" in url:
            name, song = clean_song(url, response.body)
            print(name, song)
            self.writer.writerow([name, song])
            return {"name": name, "song": song}
        
        return None
        
def start_crawl():
	#urls = [url for url in urls if url not in get_main_links()]
	try:
		process = CrawlerProcess({
				'USER_AGENT': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36'
			})
		#for url in urls:
		process.crawl(ChristmasSpider)
		process.start()
	except Exception as e:
		with open("logs/scrape_error.txt", 'a') as f:
			f.write(str(e) + "\n")