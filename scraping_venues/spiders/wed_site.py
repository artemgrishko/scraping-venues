from typing import Generator

import scrapy
from scrapy.http import Response


class WedSiteSpider(scrapy.Spider):
    name = "wed_site"
    allowed_domains = ["www.weddingwire.com"]
    start_urls = ["https://www.weddingwire.com/shared/search?group_id=1&region_id=10002&state_id=426"]

    def parse(self, response: Response, **kwargs) -> Generator:
        product_pod = response.css('.vendorTile__content.vendorTileQuickResponse__content > h2')
        for place in product_pod:
            place_detail = place.css("a::attr(href)").get()
            print(f"Place detail URL: {place_detail}")
            yield scrapy.Request(
                url=response.urljoin(place_detail),
                callback=self.parse_place_details
            )

        next_page = response.css(".pagination.app-pagination > span > button").attrib['data-href']
        if next_page:
            print(f"Next page URL: {next_page}")
            yield response.follow(next_page, callback=self.parse)
        else:
            print("No next page found.")

    def parse_place_details(self, response: Response) -> Generator:
        title = response.css(".storefrontHeading__titleWrap h1::text").get()
        description = response.css('.storefrontSummary > section > div')[1].css("p::text").getall()

        if not [text.strip() for text in description if text.strip()]:
            description = response.css(".storefrontSummary > section > div")[1].css("p > span::text").getall()

        rating = response.css(".storefrontHeadingReviews__starsValue::text").get()
        number = response.css(".storefrontAddresses__phone > span::text").get()

        if number:
            number = number.strip()
            number = number.replace("\n", "")
            number = number.replace(" ", "")
        photos = response.css('figure.storefrontMultiGallery__item.app-scroll-snap-item img::attr(src)').getall()
        location = response.css(".app-storefront-header.storefrontAddresses__header::text").getall()
        price = response.css(".storefrontHeadingFaqsCard > span::text").get()

        if price:
            price = price.strip()
            if not price.startswith("$"):
                price = ""
        else:
            price = ""

        if location:
            location = ' '.join(location)
            location = ' '.join(location.strip().title().split())

        yield {
            "title": title,
            "description": description,
            "rating": rating,
            "number": number,
            "location": location,
            "photos": photos,
            "price": price
        }
