import subprocess

from write_to_xlsx import merge_json_to_excel


def run_spider(spider_name, output_file):
    subprocess.run(['scrapy', 'crawl', spider_name, '-O', output_file])

run_spider('theknot_site', 'theknot.json')
run_spider('wed_site', 'wed.json')
run_spider('zola_site', 'zola.json')

merge_json_to_excel(
    'theknot.json',
    'wed.json',
    'zola.json',
    'result.xlsx'
)
