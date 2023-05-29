import sqlite3
from scripts import webscrapers as wb


conn = sqlite3.connect("db.sqlite3")
conn.row_factory = lambda c, row: row
c = conn.cursor()
c.execute("""SELECT url_dns, url_mvideo, url_regard
             FROM products_product""")
database_urls = c.fetchall()


for rows in database_urls:
    for url in rows:
        if "dns-shop.ru" in url:
            dns_price = wb.dns_scrape(url)

            c.execute("""UPDATE products_product
                         SET price_dns=?
                         WHERE url_dns=?""", (dns_price, url))

        elif "mvideo.ru" in url:
            mvideo_price = wb.mvideo_scrape(url)

            c.execute("""UPDATE products_product
                         SET price_mvideo = ?
                         WHERE url_mvideo=?""", (mvideo_price, url))

        elif "regard.ru" in url:
            regard_price = wb.regard_scrape(url)

            c.execute("""UPDATE products_product
                         SET price_regard=?
                         WHERE url_regard=?""", (regard_price, url))

        else:
            print("FLAG: Is the following url correct? {}".format(url))

conn.commit()
c.close()
conn.close()
