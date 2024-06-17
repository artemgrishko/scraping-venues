from typing import Generator

import scrapy
from scrapy.http import Response


class ZolaSiteSpider(scrapy.Spider):
    name = "zola_site"
    allowed_domains = ["www.zola.com"]
    start_urls = ["https://www.zola.com/wedding-vendors/search/new-york-ny--wedding-venues"]

    def parse(self, response: Response, **kwargs) -> Generator:
        product_pod = response.css(".css-1vr0ea6.e11exfs62")
        for place in product_pod:
            place_detail = place.css("a::attr(href)").get()
            print(f"Place detail URL: {place_detail}")
            yield scrapy.Request(
                url=response.urljoin(place_detail),
                callback=self.parse_place_details
            )

        next_page = response.css(".totalItemPaginationInner__MjE3N > div")[-1].css("a::attr(href)").get()
        if next_page:
            print(f"Next page URL: {next_page}")
            yield response.follow(next_page, callback=self.parse)
        else:
            print("No next page found.")

    def parse_place_details(self, response: Response) -> Generator:
        title = response.css(".hedContainer__MzMyN h1::text").get()
        description = response.css(".css-tnvgoe.e16cge80::text").get()
        rating = response.css(".css-171onha.e1wiqg192 > p::text").get()
        photos = response.css(".css-cjr941.e115mg5j32 > div.css-p11s4l.e115mg5j30 > img::attr(src)").getall()
        location = response.css(".mt-tertiary > a::text").get()
        div_elements_price = response.css(".pricing__ZjQzZ > div")

        if len(div_elements_price) > 1:
            price = div_elements_price[1].css("p::text").get()
            if price:
                price = price.strip()
                if not price.startswith("Starting"):
                    price = ""
            else:
                price = ""
        else:
            price = ""

        yield {
            "title": title,
            "description": description,
            "rating": rating,
            "location": location,
            "photos": photos,
            "price": price
        }

