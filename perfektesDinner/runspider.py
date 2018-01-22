from scrapy import cmdline

cmdline.execute("scrapy crawl dinner -o recipes.json".split())