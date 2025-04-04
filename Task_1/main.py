import redis
from redis_lru import RedisLRU

import connect
from models import Quote, Author

client = redis.StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)

@cache
def get_quotes_by_author(fullname):
    try:
        author = Author.objects(fullname__istartswith=fullname.strip()).first()
        quotes = Quote.objects(author=author.id).all()
        result = [quote.quote for quote in quotes]
        return result
    except AttributeError:
        return "There are no quotes with this author"

@cache
def get_quotes_by_tag(tag):
    quotes = Quote.objects(tags__istartswith=tag.strip()).all()
    if len(quotes) != 0:
        result = [quote.quote for quote in quotes]
        return result
    else:
        return "There are no quotes with this tag"

@cache
def get_quotes_by_tags(tags):
    tags = [tag.strip() for tag in tags.split(",")]
    quotes = Quote.objects(tags__in=tags).all()
    if len(quotes) != 0:
        result = [quote.quote for quote in quotes]
        return result
    else:
        return "There are no quotes with this tags"
    
def main():
    while True:
        command = input("Enter the command: ")
        command = command.split(':')
        if command[0] == 'exit':
            break
        elif command[0] == 'name':
            print(get_quotes_by_author(command[1]))
        elif command[0] == 'tag':
            print(get_quotes_by_tag(command[1]))
        elif command[0] == 'tags':
            print(get_quotes_by_tags(command[1]))

if __name__ == "__main__":
    main()