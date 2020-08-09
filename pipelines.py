# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient



class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy
#        db = client["jobs_db"]
 #       collection = db.collection

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        p = 0
        for ite in item["item_salary"]:
            if ite[:1].isdigit() == True and p==0:
             #   print('min_salary')
                item['min_salary']=ite
                p += 1
                if len(ite)>=5 and ite !="KZT":
                    item["currency"] = "руб."
                else:
                    item["currency"] = "уточняйте"
  #              collection.update_one({'min_salary': item['min_salary']})
            if ite[:1].isdigit() == True and p>0:
            #    print('max_salary')
                item['max_salary'] = ite
                p += 1
    #            collection.update_one({'max_salary': item['max_salary']})

        collection.insert_one(ItemAdapter(item).asdict())
        return item
#
#
#
#     def process_salary(self, salary):
#
#         min_salary,max_salary,cur = None,None,None
#         return min_salary,max_salary,cur

