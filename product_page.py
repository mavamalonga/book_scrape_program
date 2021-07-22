import requests
from bs4 import BeautifulSoup
import csv

class Extract_content:

	def __init__(self, url):
		self.product_page_url = url
		self.header = ['title', 'category', 'product_description', 'image_url',
			'universal_product_code', 'price_including_tax', 'price_excluding_tax', 
			'number_available','review_rating']

	def make_request(self):
		try:
			response = requests.get(self.product_page_url)
			self.soup = BeautifulSoup(response.content, 'html.parser')
			self.table_striped = self.soup.find_all("table", class_="table table-striped")
			self.tds = self.table_striped[0].find_all("td")
			print(f"Request successful!; status_code : {response.status_code}")
			return response.status_code
		except Exception as e:
			print(f"Failed request!; ERROR : {e}")
			return None
		
	def get_title(self):
		title = self.soup.find("title").string
		return title

	def get_category(self):
		block_ul = self.soup.find("ul", class_="breadcrumb")
		category = block_ul.find_all("a")[-1].string
		return category

	def get_description(self):
		product_description = self.soup.find(attrs={"name":"description"})["content"]
		return product_description

	def get_image_url(self):
		image_url = self.soup.find("div", id="product_gallery").find("img")["src"]
		return image_url

	def get_UPC(self):
		universal_product_code = self.tds[0].string
		return universal_product_code

	def get_price_including_tax(self):
		price_including_tax = self.tds[3].string
		return price_including_tax

	def get_price_excluding_tax(self):
		price_excluding_tax = self.tds[2].string
		return price_excluding_tax

	def get_number_available(self):
		number_available = self.tds[5].string
		return number_available

	def get_review_rating(self):
		review_rating = self.tds[-1]
		return review_rating

	def write_data_in_csv_file(self):
		try:
			with open('data.csv', 'w') as csv_file:
				writer = csv.writer(csv_file, delimiter=',')
				writer.writerow(self.header)
				writer.writerow([self.get_title(), self.get_category(), self.get_description(), 
					self.get_image_url(), self.get_UPC(), self.get_price_including_tax(), self.get_price_excluding_tax(),
					self.get_number_available(), self.get_review_rating()])
				print("Writing in the csv file was successful!")
		except Exception as e:
				print(f"writing in the csv file failed; ERROR : {e}")

	def main(self):

		status_code = self.make_request()

		if status_code == 200:
			self.write_data_in_csv_file()


inst = Extract_content("http://books.toscrape.com/catalogue/neither-here-nor-there-travels-in-europe_198/index.html")
inst.main()

