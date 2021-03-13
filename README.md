# homework-crawler
Web crawler to get information about the progress of my homeworks on the moodle2 platform.

Technologies you will need.
----
homework-crawler requires:
- [Python](https://www.python.org/downloads/release/python-366/) - Python is a programming language that lets you work quickly and integrate systems more effectively.
- [Scrapy](https://scrapy.org/) - An open source and collaborative framework for extracting the data you need from websites.

Starting the web crawler
----
[Python](https://www.python.org/downloads/release/python-366/) 3.6.6 + to run.
Download the project and start the web crawler.
Change credentials for your own credentials.
Executing this command you will start getting data and it will make a csv file with all the data it got.

  ```sh
$ scrapy crawl moodle2 -o data.csv -t csv
```

License
----
MIT


**Free Software, Hell Yeah!**
