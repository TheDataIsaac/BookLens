import scrapy
from urllib.parse import urlencode
import random
from scrapy.crawler import CrawlerProcess
from database import Database
import time
import urllib
from get import Get

# Defining a Scrapy spider for scraping book data from Amazon
class BookscraperSpider(scrapy.Spider):
    # Spider name
    name = "bookscraper"
    # Base URL and search parameters
    base_url = "https://www.amazon.com/s?"
    params = {
        "k":"data analysis",
        "rh":"n:283155",
        "crid":"33OOKCJ6AXNT6",
        "sprefix":"data analy,aps,311",
        "ref":"nb_sb_noss_2"
    }
    # List of user agents for rotating user agents
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.1',
        'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/5.0 (iPad; CPU OS 15_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0 Mobile Safari/537.36'
        ]
    # Custom settings for the spider
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 10
        } 
    # Initializing the spider with database connection and other parameters
    def __init__(self):
        # Initializing the Database class for database operations
        self.db = Database()
        self.page_num=2
        self.refr=1

    # Method to start the initial request to Amazon search results page
    def start_requests(self):
        user_agent = random.choice(self.user_agent_list)
        url=self.base_url + urlencode(self.params,doseq=True)

        print("\n",url)

 
        yield scrapy.Request(url=url, headers={'User-Agent': user_agent}, callback=self.parse)

    # Method to parse the search results page and extract book details
    def parse(self, response):
        user_agent = random.choice(self.user_agent_list)
        print("\n\n\nREF:", response.url)
        with open("res6.html","w",encoding="utf-8") as file:
            file.write(response.text)
            
        cards=response.css("div.puis-card-container")
        print("\nBooks in page: ", len(cards))
        # Loop through book cards and extract required details
        for card in cards:
            try:
                url, price, num_of_reviews = Get.get_booklinks(Get, card)
            except:
                pass
            else:
                print("\n",url)
                print(num_of_reviews)
                print(price)


                try:
                    if int(num_of_reviews) >= 100:
                        try:
                            # Follow the book URL to get detailed book information
                            yield response.follow(url=url, headers={'User-Agent': user_agent}, meta={"price":price}, callback=self.get_data)
                        except Exception as e:
                            # Handle exceptions such as 404 error
                            if response.status==404:
                                self.logger.error("Page not found: %s", response.url)
                                pass
                            else:
                                self.logger.error("Error occured: %s", str(e))
                except:
                    pass
        
        # Delay and paginate to the next search results page
        time.sleep(random.choice(range(5,15)))
        # Updated parameters for the next page
        params = {
            "k":"data analysis",
            "i":"stripbooks",
            "rh":"n:283155",
            "page":self.page_num,
            "crid":"33OOKCJ6AXNT6",
            "sprefix":"data analy,aps,311",
            "ref":f"sr_pg_{self.refr}"
        }

        headers={
            'User-Agent': user_agent,
            "Cookie" : 'session-id=138-9697947-5366151; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:NG"; ubid-main=131-8792108-0962556; session-token=+7ua45ijRKzlh21wTLr33ZqfBFA/WLNMTvxzarhyBrjjMgIcEuKx5G3iEAGSN3n5M/Y9mC8HkBFd2ic+xlxmwteinykflmGU4gbUZuKAILzZufBOLG5Cb6pGegi6XTcEzRZcYiHviBJl13hKnYDxvG7AHvvJxBo3N3qo1dRs5RBEMhztIJv8DhcNkdHLdy8ZGyMyW8PUHywWMcLwkrcO0cqE01u2b7hVmdtX7B5j/E31+QtTC/+qP+r30T6Bi3kkMsYCI35IquW0rl5YIzhky/D/3KDKhfAunMo5s8rUR/Gxz9EoTJpRuyQ0wvwXmxOPsZtyEGfVICiJDETtBuSv1xIPMw6n4Qmw; csm-hit=tb:4R9BNWXQR9JE271GXXJ6+b-TXDV82ZWS194R5VSN22T|1698073404930&t:1698073404931&adb:adblk_no',
            "Accept" : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

        next_page_url=self.base_url + urlencode(params, doseq=True)
        print("PAGE:",next_page_url)
    
        if self.page_num<=50:
            try:
                yield scrapy.Request(url=next_page_url, headers=headers, callback=self.parse)
            except Exception as e:
                print("\n\nCouldn't follow page", self.page_num,"Trying again...")
                print("Exception",e)
                try:
                    yield scrapy.Request(url=next_page_url, headers=headers, callback=self.parse, dont_filter=True)
                except Exception as e:
                    print("\n\nCouldn't follow page", self.page_num)
                    print("Exception",e)
                    self.page_num+=1
                    self.refr+=1
                    next_page_url=self.base_url + urlencode(params, doseq=True)
                    print("Going to next page:",next_page_url)
                    yield scrapy.Request(url=next_page_url, headers=headers, callback=self.parse)
            else:
                self.page_num+=1
                self.refr+=1





    # Method to extract detailed book information from the book page
    def get_data(self, response):
        with open("books7.html","w",encoding="utf-8") as file:
            file.write(response.text)

        print("\n\nSCRAPINGDATA",response.url)
        try:
            price=response.meta.get("price")[1:]
        except:
            pass
        user_agent = random.choice(self.user_agent_list)
        details=Get.get_book_data(Get, response,price)
        print(details)

        title = details["title"]
        author  = details["author"]
        description = details["description"]
        rating = details["rating"]
        num_of_rating = details["num_of_rating"]
        publisher =details["Publisher"]
        language = details["Language"]
        paperback =details["Paperback"]
        item_weight =details["Item Weight"]
        dimensions = details["Dimensions"]
        # Insert book details into the database
        try:
            insert_query="INSERT INTO books (title, author, description, rating, price, num_of_rating, publisher, language, paperback, item_weight, dimensions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"
            self.db.cur.execute(
                insert_query,
                (title, author, description, rating, price, num_of_rating, publisher, language, paperback, item_weight, dimensions)
            )
        except Exception as e:
            self.db.conn.rollback()
            raise e

        else:
            self.db.conn.commit()

            book_id=self.db.cur.fetchone()[0]
            print("\n\n\nBOOK_ID_BOOK",book_id)
            try:
                reviews_link = "https://www.amazon.com" + response.css("a[data-hook='see-all-reviews-link-foot'] ::attr(href)").get()
                print("\nREVIEWS URL:",reviews_link)
            except:
                reviews_link = "https://www.amazon.com" + response.css("span[class='cr-widget-SeeAllReviews'] div a ::attr(href)").get()
                print("\nREVIEWS URL:",reviews_link)
            # Follow the reviews link to get book reviews
            try:
                yield response.follow(url=reviews_link, headers={'User-Agent': user_agent}, meta={"book_id" : book_id}, callback=self.get_reviews)
            except:
                print("\nCOULDN'T GO TO REVIEWS PAGE")
        
    # Method to extract book reviews from the reviews page
    def get_reviews(self,response):

        with open("reviews1.html","w",encoding="utf-8") as file:
            file.write(response.text)

        book_id=response.meta.get("book_id")
        user_agent = random.choice(self.user_agent_list)

        cards=response.css("div[class='a-section review aok-relative']")
        # Extract reviews details using CSS selectors
        for card in cards:
            reviewer_name=card.css("span[class='a-profile-name'] ::text").get()
            review_rating=card.css("span[class='a-icon-alt'] ::text").get().split()[0]
            review_title=card.css("span[class='a-letter-space'] + span ::text").get().strip()
            review_date=" ".join(card.css("span[data-hook='review-date'] ::text").get().split()[-3:])
            review_content=card.css("span[data-hook='review-body'] span ::text").get()

            print({"reviewer_name":reviewer_name,
                   "review_rating":review_rating,
                   "review_title":review_title,
                   "review_date":review_date,
                   "review_content":review_content}
            )
            try:
                print("\n\n\nBOOK_ID_REVIEW",book_id)
                # Insert review details into the database
                insert_query= "INSERT INTO reviews (reviewer_name, review_rating, review_title, review_date, review_content, book_id) VALUES (%s, %s, %s, %s, %s, %s);"
                self.db.cur.execute(
                    insert_query,
                    (reviewer_name, review_rating, review_title, review_date, review_content, book_id)
                )
            except Exception as e:
                self.db.conn.rollback()
                raise e
            else: 
                self.db.conn.commit()

        headers={
            'User-Agent': user_agent,
            "Cookie" : 'session-id=138-9697947-5366151; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:NG"; ubid-main=131-8792108-0962556; session-token=YOlOkj2MlaikZvtVrSRELO6n0eUbZqZPDLkH5PZpYuIbyvMEGQ2be25ihyqS4JzdDnkW0gj6D1tNQOCrvNZ1H95i0oeqvbMUyWNi3odDEFL8UqaPXNtuhMtEWWVXYMwRR4doi23202Rpfbr2Ne6bs30G55XvNuY5uLi+JdcsMD01KOnBPVv1teuknsuQK89YjbIOhxiAaRP0k6IkBwpbn9S/LoZgySLX74Gy7uwfZnLTbIG0oKApjEA+BsZp53jtX+oeLeg31pYwlYffxqe9/1n7szzsEsGBtkNSnRZ4PhfstddogDY3ErnJ37EgcCgRMW68Udywooq+sl6gjX7gVBwLEV1Zzplp; csm-hit=tb:BNKH0RZZ875AC0H3YSST+s-WNYA1KK4PP16H7B2EREE|1698077078262&t:1698077078262&adb:adblk_no'
        }

        time.sleep(random.choice(range(4,10)))

        print("\n",response.url)
        pagination=response.css("ul[class='a-pagination']")
        next_page=pagination.css("a  ::attr(href)").get()
        if next_page:
            next_page="https://www.amazon.com" + next_page
            try:
                if "to=" not in next_page:
                    # Follow the next page link to get more reviews
                    print("\nREVIEWS NEXT URL",next_page)
                    yield response.follow(url=next_page, headers=headers, meta={"book_id" : book_id}, callback=self.get_reviews)
                else:
                    next_page=next_page.split("to=")[1].split("&openid")[0]
                    next_page=urllib.parse.unquote(next_page)
                    print("\nREVIEWS NEXT URL",next_page)
                    yield response.follow(url=next_page, headers=headers, meta={"book_id" : book_id}, callback=self.get_reviews)
            except:
                pass


    
    # Method to close the spider and database connections
    def close(self):
        self.db.cur.close()
        self.db.conn.close()


# Main block to run the spider
if __name__ == "__main__":
    # Initialize and start the crawler process
    process = CrawlerProcess()
    process.crawl(BookscraperSpider)
    process.start()
