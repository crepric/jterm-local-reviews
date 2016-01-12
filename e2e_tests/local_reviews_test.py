from selenium import webdriver
import unittest

class MainPageTests(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('localhost:27080')

    def tearDown(self):
        self.browser.close()

    def testContent(self):
        self.assertIn('Northampton Local Guide', self.browser.title)
        body = self.browser.find_element_by_tag_name('body')
        mainheader = self.browser.find_element_by_id('mainheader')
        self.assertEqual("Welcome to your best guide to Northampton, MA",
                         mainheader.text)
        self.assertIn('Northampton Local Guide', self.browser.title)

    def testIncreaseVotes(self):
        reviews = self.browser.find_elements_by_class_name('review')
        for review in reviews:
            like_counts_before = review.find_element_by_class_name('like_count').text
            other_reviews = set(reviews) - set([review])
            other_reviews_counters = {}
            for other_review in other_reviews:
                other_reviews_counters[other_review] = (
                    int(other_review.find_element_by_class_name('like_count').text))
            plus_button = review.find_element_by_class_name('likebutton')
            plus_button.click()
            like_counts_after = review.find_element_by_class_name('like_count').text
            self.assertEqual(1, int(like_counts_after)- int(like_counts_before))
            for other_review in other_reviews:
                self.assertEqual(other_reviews_counters[other_review],
                    int(other_review.find_element_by_class_name('like_count').text))

    def testDecreaseVotes(self):
        reviews = self.browser.find_elements_by_class_name('review')
        for review in reviews:
            like_counts_before = review.find_element_by_class_name('like_count').text
            other_reviews = set(reviews) - set([review])
            other_reviews_counters = {}
            for other_review in other_reviews:
                other_reviews_counters[other_review] = (
                    int(other_review.find_element_by_class_name('like_count').text))
            minus_button = review.find_element_by_class_name('dislikebutton')
            minus_button.click()
            like_counts_after = review.find_element_by_class_name('like_count').text
            self.assertEqual(-1, int(like_counts_after)- int(like_counts_before))

    def testSorted(self):
        sorted_check = self.browser.find_element_by_id('chk_sorted_order_reverse')
        self.assertFalse(sorted_check.get_attribute('checked'))
        sort_button = self.browser.find_element_by_id('btn_sort')
        sort_button.click()
        reviews = self.browser.find_elements_by_class_name('review')
        prev_value = int(reviews[0].find_element_by_class_name('like_count').text)
        for review in reviews:
            like_counts = int(review.find_element_by_class_name('like_count').text)
            self.assertGreaterEqual(like_counts, prev_value)

    def testSortedDescending(self):
        sorted_check = self.browser.find_element_by_id('chk_sorted_order_reverse')
        sorted_check.click()
        self.assertTrue(sorted_check.get_attribute('checked'))
        sort_button = self.browser.find_element_by_id('btn_sort')
        sort_button.click()
        reviews = self.browser.find_elements_by_class_name('review')
        prev_value = int(reviews[0].find_element_by_class_name('like_count').text)
        for review in reviews:
            like_counts = int(review.find_element_by_class_name('like_count').text)
            self.assertLessEqual(like_counts, prev_value)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(MainPageTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
