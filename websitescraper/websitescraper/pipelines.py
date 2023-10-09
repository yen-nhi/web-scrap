# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from websitescraper import settings
import mysql.connector
from itemadapter import ItemAdapter



class CleanItemPipeline:
    """
    Clean and format item data
    """
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if type(value) is tuple:
                value = value[0]
            if value:
                adapter[field_name] = value.strip()
                if field_name == 'price':
                    cleaned_price = ''.join(i for i in value if ord(i) < 128)
                    adapter[field_name] = float(cleaned_price.replace(',', '.'))
                elif field_name == 'volume':
                    adapter[field_name] = float(value)

            # rating has the case None
            if field_name == 'rating':
                if value:
                    adapter[field_name] = float(value)
                else:
                    adapter[field_name] = 0

        return item


class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS douglas_items(
            id int NOT NULL auto_increment, 
            product_name VARCHAR(255),
            brand VARCHAR(255),
            price DECIMAL,
            category VARCHAR(255),
            volume DECIMAL,
            rating DECIMAL, 
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute(""" insert into douglas_items (
                    product_name, 
                    brand, 
                    price, 
                    category, 
                    volume,
                    rating
                    ) values (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                        )""", (
            item["name"],
            item["brand"],
            item["price"],
            item["category"],
            item["volume"],
            item["rating"]
        ))

        ## Execute insert of data into database
        self.conn.commit()

    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cur.close()
        self.conn.close()



