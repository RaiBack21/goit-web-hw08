import connect
import json
from datetime import datetime

from models import Author, Quote

with open('authors.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    author = Author(fullname = item['fullname'], 
                    born_date = datetime.strptime(item['born_date'], "%B %d, %Y"), 
                    born_location = item['born_location'],
                    description = item['description'])
    author.save()

with open('quotes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    author = Author.objects(fullname=item['author']).first()
    quote = Quote(tags = item['tags'], author = author.id, 
                  quote = item['quote'])
    quote.save()