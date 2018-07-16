import scrapy
from scrapy.contrib.spiders.init import InitSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from nugo.items import Homework

# credentials
USER_NAME = 'YOUR-PLATFORM-USERNAME'
PASSWORD  = 'YOUR-PLATFORM-PASSWORD'

class Moodle2Spider(InitSpider):
    name = 'moodle2'
    allowed_domains = ['moodle2.cucei.udg.mx']
    start_urls = 'http://moodle2.cucei.udg.mx/login/index.php'

    def init_request(self):
       #"""This function is called before crawling starts."""
       return Request(url=self.start_urls, callback=self.login)

    def login(self, response):
        #"""Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'username': USER_NAME, 'password': PASSWORD},
                    callback=self.check_login_response, dont_filter = True)

    def check_login_response(self, response):
        name =  response.css(".usertext::text").extract()
        if len(name) != 0:
            print("\n\n************************************************\n\n")
            print("\n\n               YOU ARE LOG IN \n\n")
            print("\n\n************************************************\n\n")

            return FormRequest.from_response(response, callback=self.parse, dont_filter = True)

        else:
            print("\n\n************************************************\n\n")
            print("\n\n               LOG IN FAILED \n\n")
            print("\n\n************************************************\n\n")

    def parse(self, response):
        #"""This function gets all the course's link"""
        urls = response.xpath('//h2[contains(@class, "title")]/a//@href').extract()
        for u in urls:
            yield Request(
                        url=u,
                        method='GET',
                        callback=self.obtainGradeLink
                    )

    def obtainGradeLink(self, response):
        #"""This function gets all the course's grade links."""
        links = response.xpath('//li[contains(@class, "type_setting collapsed item_with_icon")]/p/a//@href').extract()
        for l in links:
            yield Request(
                        url=l,
                        method='GET',
                        callback=self.parse_items
                    )

    def parse_items(self, response):
        #"""This function gets all the homework's link"""
        links = response.xpath('//th[contains(@class, "item b1b column-itemname")]/a//@href').extract()
        for l in links:
            yield Request(
                        url=l,
                        method='GET',
                        callback=self.exctractInfo
                    )

    def exctractInfo(self, response):
        #"""This function gets all the data of the homework."""
        homework = Homework()
        homework['subject'] = response.xpath('//p[contains(@class, "tree_item branch")]/a//@title').extract_first()
        homework['name'] = response.xpath('//div[contains(@role, "main")]/h2//text()').extract()
        homework['submission_status'] = response.xpath('//td[contains(@class, "submissionstatussubmitted")]/text()').extract()
        homework['submission_graded'] = response.xpath('//td[contains(@class, "submissiongraded")]/text()').extract()
        homework['submission_date'] = response.xpath('//td[contains(text(), "Fecha")]//following-sibling::td/text()').extract()
        homework['left_time'] = response.xpath('//td[contains(@class, "earlysubmission")]/text()').extract()
        homework['last_modification'] = response.xpath('//td[contains(text(), "Última")]//following-sibling::td/text()').extract()
        homework['grade'] = response.xpath('//div[contains(@class, "feedback")]/div/table/tbody/tr[1]/td[2]/text()').extract()
        yield homework
