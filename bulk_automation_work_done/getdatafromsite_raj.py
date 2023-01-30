from ntpath import join
import scrapy
from datetime import datetime,timedelta
from urllib.parse import urlparse
import os
import csv
import mysql.connector


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    #FilePath="D:\\work\\python\\webscrape\\"
    mydb = mysql.connector.connect(
            host="64.227.176.243",
  user="phpmyadmin",
  password="Possibilities123.@",
  database="url_automation")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bulk_quill_bank where Category is null and bqt_id = 4")
    myresult = mycursor.fetchall()
    #read url csv file
    #urlCsvFile = open(join(FilePath,"sitemapurl.csv"))
    #csvreader = csv.reader(urlCsvFile)
    rows = []
    #for row in csvreader:
    #    rows.append(row)
        #print(row)
    #urlCsvFile.close()  
    def start_requests(self):
        #urls = [
        #    'https://www.hitc.com/feed/',
        #    'https://dmerharyana.org/feed/'
        #]
        #urls=self.rows
        for url in self.myresult:
            print(url)
            yield scrapy.Request(url=url[1], meta={'bqt_id':url[6],'wcid':url[0]}, callback=self.parse)

    def parse(self, response):
        domain = urlparse(response.url).netloc
        #print(response.xpath('//h1[@class="tdb-title-text"]').get())
        #print(response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " td-post-content ")]').get(default='not-found'))
        self.mycursor.execute("SELECT * FROM bulk_quill_template where bqt_id=4")
        myresult = self.mycursor.fetchone()
        if not myresult:
          exit
        # webTitle= response.xpath(myresult[2]).get()
        # print(webTitle)
        content=response.xpath(myresult[5]).get()
        # content=response.xpath(myresult[3]).get()
        # image_link= response.css(myresult[4]).get()
        #data = [webTitle, content]
        
        mycursor = self.mydb.cursor()
        # sql = "update bulk_quill set title=%s,content=%s,featured_image=%s where wcid=%s"
        sql = "update bulk_quill_bank set Category=%s where wcid=%s"
        # val = (webTitle,content,image_link,response.meta['wcid'])
        val = (content,response.meta['wcid'])
        mycursor.execute(sql, val)
        self.mydb.commit()
        #with open('WebsiteContent.csv', 'w', encoding='UTF8', newline='') as f:
            #writer = csv.writer(f)
            # write the data
            #writer.writerow(data)
    #def closed(self, reason):
    #    ft = open(self.FilePathName, "w", encoding='utf-8')
    #    ft.write(self.LatestDate.strftime("%Y-%m-%d %H:%M:%S"))
    #    ft.close()
        