from scrapy.http import HtmlResponse

html1 = open('example1.html', encoding='utf-8').read()
html2 = open('example2.html', encoding='utf-8').read()

response1 = HtmlResponse(url='http://example1.com', body=html1, encoding='utf8')
response2 = HtmlResponse(url='http://example2.com', body=html2, encoding='utf8')

from scrapy.linkextractors import LinkExtractor

get_urls = lambda link: link.url

# Extract all urls
le    = LinkExtractor()
links = le.extract_links(response1)
urls1 = list(map(get_urls, links))

# Extract urls matches pattern (allow)
pattern = '/intro/.+\.html$'
le      = LinkExtractor(allow=pattern)
links   = le.extract_links(response1)
urls2   = list(map(get_urls, links))

# Exclude urls matches pattern (deny)
from urllib.parse import urlparse

patten = '^' + urlparse(response1.url).geturl()
le     = LinkExtractor(deny=pattern)
links  = le.extract_links(response1)
urls3  = list(map(get_urls, links))

# Extract urls from domains (allow_domains)
domains = ['github.com', 'stackoverflow.com']
le      = LinkExtractor(allow_domains=domains)
links   = le.extract_links(response1)
urls4   = list(map(get_urls, links))

# Exclude urls from domains (deny_domains)
le    = LinkExtractor(deny_domains='github.com')
links = le.extract_links(response1)
urls5 = list(map(get_urls, links))

# (restrict_xpaths)
le    = LinkExtractor(restrict_xpaths='//div[@id="top"]')
links = le.extract_links(response1)
urls6 = list(map(get_urls, links))

# (restrict_css)
le    = LinkExtractor(restrict_css='div#bottom')
links = le.extract_links(response1)
urls7 = list(map(get_urls, links))

# (tags)
# 接收 标签 (字符串) 或 标签 列表, 提取 指定 标签内 的 链接, 默认 为 ['a', 'area']

# (attrs)
le    = LinkExtractor(tags='script', attrs='src')
links = le.extract_links(response2)
urls8 = list(map(get_urls, links))

# process_value (callback function)
#
# returns string or None
import re

def process(value):
    match = re.search("javascript:goToPage\('(.*?)'", value)

    if match:
        value = match.group(1)

    return value

le = LinkExtractor(process_value=process)
links = le.extract_links(response2)
urls9 = list(map(get_urls, links))
