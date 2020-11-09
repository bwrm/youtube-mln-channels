from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from vars import *
from selenium.webdriver.common.keys import Keys


lang_list = ['382', '381', '105', '383', '9', '58', '11', '14', '384', '29', '19', '385', '54', '27', '22', '386',
             '141', '24', '388', '389', '23', '100', '10', '390', '391', '449', '450', '392',
             '25', '48', '50', '395', '1', '32', '396', '397', '57', '62', '60', '59', '17', '398', '55', '416',
             '63', '21', '401', '46', '65', '400', '402', '67', '403', '404', '78', '71', '405', '68', '77', '408',
             '69', '406', '407', '410', '409', '73', '37', '82', '411', '413', '414', '83', '412', '85', '126', '440',
             '87', '415', '84', '418', '139', '93', '417', '41', '91', '92', '98', '95', '31', '419', '99', '70', '118',
             '420', '103', '101', '117', '421', '116', '33', '423', '56', '425', '424', '4', '422', '74', '125', '6',
             '426', '30', '427', '94', '428', '15', '16', '35',
             '429', '430', '399', '26', '393', '435', '153', '431', '432', '434', '49', '433', '127', '13', '436',
             '43', '8', '437', '439', '132', '72', '441', '438', '131', '387', '51', '154', '144', '34', '47', '5',
             '442', '137', '120', '138', '145', '140', '443', '444', '394', '445', '146', '446', '447', '448', '147']


class YoucrawlSpider:

    name = 'youcrawl'
    start_url = "https://www.channelcrawler.com/"
    chrome_options = Options()
    driver = webdriver.Chrome("/home/s/prog/chromedriver", options=chrome_options)

    def __init__(self):
        self.out_file = open('data.csv', 'a+')

    @staticmethod
    def _main_page_form_papulation(driver, data):
        driver.find_element_by_xpath(
            '/html/body/div/div[3]/div/div[1]/div[1]/form/div[2]/div[2]/div[1]/div/div[1]/input').clear()
        driver.find_element_by_xpath(
            '/html/body/div/div[3]/div/div[1]/div[1]/form/div[2]/div[2]/div[1]/div/div[1]/input').send_keys('1000000')
        sleep(0.1)
        driver.find_element_by_xpath(
            '//*[@id="queryIndexForm"]/div[2]/div[1]/div[3]/div/div/div[1]/div/span/input').send_keys(Keys.BACKSPACE)
        sleep(0.5)
        driver.find_element_by_xpath(
            f'//*[@id="queryIndexForm"]/div[2]/div[1]/div[3]/div/div/div[2]/ul/li[@data-value="{data}"]').click()
        sleep(0.5)
        driver.find_element_by_xpath(
            '//*[@id="queryIndexForm"]/div[2]/div[1]/div[3]/div/div/div[1]/div/span/input').send_keys(Keys.ENTER)
        return True

    def load_channels_list(self, chan_id):
        self.driver.get(self.start_url)
        self._main_page_form_papulation(self.driver, chan_id)
        sleep(2)

    def get_page_source(self):
        return self.driver.page_source

    def parse_data_from_page(self, selector):
        return self.driver.find_element_by_xpath(selector)

    def is_next_page(self):
        try:
            return self.driver.find_element_by_xpath('//li[@class="next"]/a')
        except ValueError:
            print("Next page is not found")

    def save_list_to_file(self, *args):
        out_result_string = ",".join(*args)
        self.out_file.write(out_result_string)

    def channel_parse(self):
        sel = Selector(text=self.driver.page_source)
        print(sel.text)

    def close_driver(self):
        self.driver.quit()


if __name__ == '__main__':

    for country_id in lang_list:
        page = YoucrawlSpider()
        page.load_channels_list(country_id)
        while True:
            titles = page.driver.find_elements_by_xpath('//div[@class="channel col-xs-12 col-sm-4 col-lg-3"]/h4/a')
            channels_url = page.driver.find_elements_by_xpath(
                '//div[@class="channel col-xs-12 col-sm-4 col-lg-3"]/h4/a')
            category = page.driver.find_elements_by_xpath('//div[@class="channel col-xs-12 col-sm-4 col-lg-3"]/small/b')
            other_info = page.driver.find_elements_by_xpath(
                '//div[@class="channel col-xs-12 col-sm-4 col-lg-3"]/p/small')

            for title, channel, category, other_info in zip(titles, channels_url, category, other_info):
                title = title.get_attribute("title")
                channel_url = channel.get_attribute("href")
                cat = category.text
                another = other_info.text
                another = another.replace('\n', '')
                page.save_list_to_file([title, channel_url, cat, another + '\n'])

            next_page = page.is_next_page()
            if next_page:
                print('read next page')
                next_page.click()
            else:
                break






