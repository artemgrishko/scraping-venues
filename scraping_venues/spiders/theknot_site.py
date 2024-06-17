from typing import Generator

import scrapy
from scrapy.http import Response


class TheknotSiteSpider(scrapy.Spider):
    name = "theknot_site"
    allowed_domains = ["www.theknot.com"]
    start_urls = ["https://www.theknot.com/marketplace/wedding-reception-venues-new-york-ny"]

    def parse(self, response: Response, **kwargs) -> Generator:
        product_pod = response.css(
            ".col-12--71dcc.col-md-6--3db49.col-xxl-4--80f68.new-vendor-card-column--482e2.card-column--f29c5")
        for place in product_pod:
            place_detail = place.css(".content-large--d9936 > a::attr(href)").get()
            print(place_detail)
            yield scrapy.Request(
                url=response.urljoin(place_detail),
                callback=self.parse_place_details
            )

        next_page = response.css(".container--d15d7 > li")[-1].css("a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_place_details(self, response: Response) -> Generator:
        title = response.css(".vendor-name-container--42c4a h1::text").get()
        description = response.css(".desc--f5f28.body1--e44d4::text").get()
        rating = response.css(".reviews-details-star-count--3642f.h2--b75a9::text").get()
        number = response.xpath(
            '//*[@id="navContact"]/div/div/div[2]/div/div/div[1]/span[2]/div/a/div/div/text()').get()
        location = response.xpath('//*[@id="navContact"]/div/div/div[2]/div/div/div[1]/span[1]/text()').get()

        photo1 = response.css(".full-column--74061 > button > img::attr(src)").getall()
        photo2 = response.css(
            ".col-3--721d7.col-lg-2--857de.gallery-column--ff2c0.half-column--b0319 > div.row--a6f92 > div.col-12--71dcc > button > img::attr(src)").getall()
        photo3 = response.css(
            ".col-6--b81fd.col-lg-4--4691c.gallery-column--ff2c0.wide-column--6d616.rounded-edge-right--ab60b > button > img::attr(src)"
        ).get()

        photos = []
        if photo1 and isinstance(photo1, list):
            photos.extend(photo1)
        if photo2 and isinstance(photo2, list):
            photos.extend(photo2)
        if photo3 and isinstance(photo3, list):
            photos.append(photo3)

        yield {
            "title": title,
            "description": description,
            "rating": rating,
            "number": number,
            "location": location,
            "photos": photos
        }
