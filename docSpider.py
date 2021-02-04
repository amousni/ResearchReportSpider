from selenium import webdriver
from lxml import etree
import ssl
import json
import os
import time
from xf_ocr import xf_get_word
from PIL import Image

ssl._create_default_https_context = ssl._create_unverified_context

chromedriver = '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/selenium/chromedriver'

class Cookies(object):
	def __init__(self,driver):
		self.driver=driver
 
	#获取cookies保存到文件
	def save_cookie(self, cookie_name):
		cookies=self.driver.get_cookies()
		json_cookies=json.dumps(cookies)
		with open(cookie_name,'w') as f:
			f.write(json_cookies)

	def add_cookie(self, cookie_name):
		self.driver.delete_all_cookies()
		dict_cookies={}
		with open(cookie_name, 'r', encoding='utf-8') as f:
			list_cookies = json.loads(f.read())
		for i in list_cookies:
			# print(i)
			self.driver.add_cookie(i)


def junk_register():
	browser = webdriver.Chrome(executable_path=chromedriver)
	junk_mails = ["j" + str(i+1) + "@40oz.cc" for i in range(19)]

	for i in junk_mails:
		browser.get("http://www.51pdf.cn/user/register.aspx")
		browser.find_element_by_xpath("//table/tbody/tr/td[@class='inbox']/input[@id='ctl00_web_center_email']").send_keys(i)
		browser.find_element_by_xpath("//table/tbody/tr/td[@class='inbox']/input[@id='ctl00_web_center_password']").send_keys("Amous0908")
		browser.find_element_by_xpath("//table/tbody/tr/td[@class='inbox']/input[@id='ctl00_web_center_confirmPassword']").send_keys("Amous0908")

		time.sleep(6)

		browser.find_element_by_xpath("//div[2]/div[2]/div[@class='sigin_zone'][4]/input[@id='ctl00_web_center_checkbtn']").click()

	browser.close()


def obtain_cookies():
	browser = webdriver.Chrome(executable_path=chromedriver)
	junk_accounts = ["j" + str(i+1) + "@40oz.cc" for i in range(19)]
	accounts = ["amousni@pku.edu.cn", "1901213177@pku.edu.cn", "1500017774@pku.edu.cn", "pku@40oz.cc", "B2Purple@40oz.cc", "54443279@qq.com", "amousni@foxmail.com"]
	accounts = accounts + junk_accounts

	for i in range(len(accounts)):
		while True:
			browser.get("http://www.51pdf.cn/user/userlogin.aspx")

			browser.find_element_by_xpath("//tbody/tr[1]/td[2]/input[@id='ctl00_web_center_EmailTxt']").send_keys(accounts[i])
			browser.find_element_by_xpath("//table/tbody/tr[3]/td[2]/input[@id='ctl00_web_center_PassTxt']").send_keys("Amous0908")

			browser.save_screenshot('page.png')
			code_img_ele = browser.find_element_by_xpath("//div[2]/div/table/tbody/tr[5]/td[2]/img[@id='ctl00_web_center_checkcode']")
			rangle = (960, 790, 1090, 845)
			image = Image.open('./page.png')
			frame = image.crop(rangle)
			frame.save('code.png')
			vcode = xf_get_word('./code.png')
			if len(str(vcode)) == 4:
				browser.find_element_by_xpath("//div/table/tbody/tr[5]/td[2]/input[@id='ctl00_web_center_checkcodes']").send_keys(str(vcode))
				browser.find_element_by_xpath("//div/table/tbody/tr[8]/td/input[@id='ctl00_web_center_SubMit']").click()

				html = browser.page_source
				r = etree.HTML(html)
				if len(r.xpath("/div[2]/div/table/tbody/tr[8]/td/span[@id='ctl00_web_center_Message']")) == 0:
					cookie_name = './COOKIES/cookie_' + str(i) + '.json'
					cookies_manager = Cookies(browser)
					cookies_manager.save_cookie(cookie_name)
					browser.delete_all_cookies()
					break
				else:
					continue
			else:
				continue
		# browser.close()

def doc_url_spider(base_url = "http://www.51pdf.cn/search.aspx?si=99&ft=0&keyword=%u50A8%u80FD&page=", pages = 11):
	browser = webdriver.Chrome(executable_path=chromedriver)
	browser.get("http://www.51pdf.cn/user/userlogin.aspx")
	cookies_manager = Cookies(browser)
	cookies_name = ['./COOKIES/cookie_' + str(i) + '.json' for i in range(6)]

	cookies_manager.add_cookie(cookies_name[0])

	url_list = []

	for page in range(pages):
		url = base_url + str(page+1)
		browser.get(url)
		html = browser.page_source
		r = etree.HTML(html)
		temp_url_list = r.xpath("//table[@id='ctl00_web_center_gdv']/tbody/tr/td[@class='rlist']/a/@href")
		url_list = url_list + temp_url_list
		print(len(temp_url_list))
		time.sleep(2)

	browser.close()

	for i in range(len(url_list)):
		url_list[i] = 'http://www.51pdf.cn' + url_list[i]

	with open('url_list.txt', 'w') as f:
		f.write('\n'.join(url_list))

def doc_spider():
	browser = webdriver.Chrome(executable_path=chromedriver)
	browser.get("http://www.51pdf.cn/user/userlogin.aspx")
	cookies_manager = Cookies(browser)
	cookies_name = ['./COOKIES/cookie_' + str(i) + '.json' for i in range(26)]

	ready_docs = os.listdir('./docs')
	with open('./url_list.txt', 'r') as f:
		url_list = f.read().split()

	while len(url_list) != 0 and len(cookies_name) != 0:
		print('======using cookie: {}======'.format(cookies_name[0]))
		cookies_manager.add_cookie(cookies_name[0])
		browser.get(url_list[0])
		html = browser.page_source
		r = etree.HTML(html)
		doc_name = r.xpath("//table[@class='f12']/tbody/tr/td[1]/table[1]/tbody/tr[1]/td[2]/h4/text()")[0] + '.pdf'
		if doc_name in ready_docs:
			print('{} in docs'.format(doc_name))
			url_list.pop(0)
			continue

		browser.find_element_by_xpath("//tbody/tr/td[1]/table[1]//td/a/img").click()
		html = browser.page_source
		r = etree.HTML(html)

		if len(r.xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/strong/text()")) != 0:
			print('{} loss effiency'.format(cookies_name[0]))
			cookies_name.pop(0)
		else:
			time.sleep(5)
			print('{} is downloaded'.format(doc_name))
			url_list.pop(0)

	print('-'*30)
	print("remain docs: {}".format(len(url_list)))
	print("remain cookies: {}".format(len(cookies_name)))
	browser.close()


def main():
	# junk_register()
	# obtain_cookies()
	# doc_url_spider()
	doc_spider()
	

if __name__ == '__main__':
	main()












