import scrapy
import w3lib.html

from ..items import RitchieItem


class RitchieSpiderSpider(scrapy.spiders.SitemapSpider):
    name = "ritchie_spider"
    allowed_domains = ["www.ritchiespecs.com"]
    sitemap_urls = ["https://www.ritchiespecs.com/sitemap.xml"]
    sitemap_rules = [('/model', 'parse_equipment')]

    def parse_equipment(self, response):
        item = RitchieItem()
        model = response.css('h1::text').get()
        equipment_dict = dict()

        # Bucket, Dimensions, Engine, Operational, Transmission, Hydraulic, ...
        sections = response.css('h3::text').getall()
        for section in sections:

            # <div>BUCKET</div> ...
            sec_name_tag = response.xpath(f'//h3[text()="{section}"]/parent::div/parent::div')
            specs_dict = dict()

            # HTML Span tags of current section [Bucket -> Breakout Force, Bucket Capacity - Heaped, ...]
            features = sec_name_tag.css('h4::text').getall()
            for index in range(0, len(features)):
                feature_name = features[index]  # Breakout Force
                value = sec_name_tag.css('span.space')[index].get()  # 9172
                unit = sec_name_tag.css('span.space + span')[index].get()  # lb or span_tags

                values_fmt = f'{w3lib.html.remove_tags(value)} {w3lib.html.remove_tags(unit)}'  # 9172 lb

                specs_dict[feature_name] = values_fmt.strip()

            equipment_dict[section.strip()] = specs_dict

        item['model_name'] = model
        item['specs'] = equipment_dict

        yield item
