from scrapy.selector import Selector
from scrapy.http import HtmlResponse

body = '''
<html>
  <head>
    <base href="http://example.com/" />
    <title>Example website</title>
  </head>

  <body>
    <div id="images">
      <a href="image1.html">Name: Image 1 <br /><img class="thumb" src="image1.jpg" /><strong>tail</strong></a>
      <a href="image2.html">Name: Image 2 <br /><img class="thumb" src="image2.jpg" /></a>
      <a href="image3.html">Name: Image 3 <br /><img src="image3.jpg" /></a>
      <a href="image4.html">Name: Image 4 <br /><img src="image4.jpg" /></a>
      <a href="image5.html">Name: Image 5 <br /><img src="image5.jpg" /></a>
    </div>

    <p>Below is empty paragraph: </p>
    <p></p>
  </body>
</html>
'''

response = HtmlResponse(url='http://www.example.com', body=body, encoding='utf8')
