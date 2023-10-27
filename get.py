class Get:
    def get_booklinks(self, card):
        try:
            url=card.css("a[class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'] ::attr(href)").get()
            url=self.process_url(self,url)
        except:
            try:
                url=card.css("a[title='product-detail'] ::attr(href)").get()
                if "sspa" in url:
                    print("\nprocessed url")
                    url=self.process_url(self, url)
            except:
                print("Couldn't get book url",e)
        try:
            num_of_reviews=card.css("span[class='a-size-mini a-color-base puis-light-weight-text'] ::text").get().replace(",","").replace("(","").replace(")","")
        except:
            try:
                num_of_reviews=card.css("span[class='a-size-base s-underline-text'] ::text").get().replace(",","")
            except:
                print("Couldn't get number of reviews",e)
        try:
            price=card.css("span[class='a-offscreen'] ::text").get()
        except Exception as e:
            print("Couldn't get book price",e)

        return url, price, num_of_reviews
    



    def get_book_data(self, response,price):
        # Extract book details using CSS selectors
        try:
            title=response.css("span[id='productTitle'] ::text").get().strip()
        except:
            try:
                title=response.css("h1[id='title'] ::text").get().strip()
            except:
                print("Couldn't get book title")
        else:
            if title=="":
                try:
                    title=response.css("h1[id='title'] ::text").get().strip()
                except:
                    print("Couldn't get book title")


        try:
            author=", ".join(response.css("span.author a ::text").getall()).strip()
        except:
            try:
                author=", ".join(response.css("a[id='bylineContributor'] ::text").getall()).strip()
            except:
                print("Couldn't get book author")
        else:
            if author=="":
                try:
                    author=", ".join(response.css("a[id='bylineContributor'] ::text").getall()).strip()
                except:
                    print("Couldn't get book author")


        try:
            description=" ".join(response.css("div[data-a-expander-name='book_description_expander'] *::text").getall()[:-2]).strip()
            
        except:
            try:
                description = [item.strip() for item in response.css('p span::text, ul li span::text').getall() if item.strip()][8:-12]
                description = ' '.join(description)
            except:
                print(" Couldn't get book description")
        else:
            if description=="":
                try:
                    description = [item.strip() for item in response.css('p span::text, ul li span::text').getall() if item.strip()][8:-12]
                    description = ' '.join(description)
                except:
                    print(" Couldn't get book description")

                    
        try:
            rating=response.css("a[class='a-popover-trigger a-declarative'] span[class='a-size-base a-color-base'] ::text").get().strip()
        except:
            try:
                rating=response.css("span[class='a-size-base a-color-base'] ::text").get().strip()
            except:
                print("Couldn't get book rating")
        else:
            if rating=="":
                try:
                    rating=response.css("span[class='a-size-base a-color-base'] ::text").get().strip()
                except:
                    print("Couldn't get book rating")

        try:
            num_of_rating=response.css("span[id='acrCustomerReviewText'] ::text").get().split()[0].replace(",","")
        except:
            try:
                num_of_rating=response.css("span[class='a-size-base cm-cr-review-stars-text-xsm'] ::text").get().strip().replace(",","")
            except:
                print("Couln't get number of ratings")
        else:
            if num_of_rating=="":
                try:
                    num_of_rating=response.css("span[class='a-size-base cm-cr-review-stars-text-xsm'] ::text").get().strip().replace(",","")
                except:
                    print("Couln't get number of ratings")


        try:
            book_details=response.css("div[id='detailBullets_feature_div']")
        except:
            try:
                book_details = response.css('table#productDetails_techSpec_section_1 tr')
            except:
                print("Couldn't get book details")
        else:
            details_subset={}
            if not book_details:
                try:
                    book_details = response.css('table#productDetails_techSpec_section_1 tr')
                except:
                    print("Couldn't get book details")     

            try:
                for data in book_details.css("li span[class='a-list-item']"):
                    try:
                        detail_key=data.css("span[class='a-text-bold'] ::text").get().split("\n")[0].strip()
                        detail_value=data.css("span[class='a-text-bold'] + span ::text").get()
                    except:
                        pass
                    else:
                        if detail_key and detail_value:
                            details_subset[detail_key]=detail_value
            except:
                pass
            else:
                if not details_subset:
                    try:
                        for data in book_details:
                            try:
                                detail_key=data.css("th[class='a-span3 prodDetSectionEntry'] ::text").get()
                                detail_value=data.css("span ::text").get().strip(" ' \u200e")
                            except:
                                pass
                            else:
                                if detail_key and detail_value:
                                    details_subset[detail_key]=detail_value
                    except Exception as e:
                        print(e)
        # Define the book details dictionary
        details_subset={key.strip(): value for key, value in details_subset.items()}    
        details={
            "title":title,
            "author":author,
            "description":description,
            "rating":rating,
            "price":price,
            "num_of_rating":num_of_rating
        }
        
        details.update(details_subset)
        return details


    def process_url(self, input_url):
        # Split the input URL with "url="
        url_parts = input_url.split("url=")
        
        # Take the last part of the split URL and decode special characters
        last_part = url_parts[-1].replace("%2F", "/").replace("%3D", "=").replace("%3F", "?")
        
        # Split with "id%3D" and return the first part
        result_parts = last_part.split("id")
        return "https://www.amazon.com" + result_parts[0]
    


if __name__=="__main__":
    pass