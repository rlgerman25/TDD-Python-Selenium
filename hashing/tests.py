from django.test import TestCase
from selenium import webdriver
from .forms import HashForm
from .models import Hash
import hashlib
from django.core.exceptions import ValidationError
import time

PATH = '/Users/ronardlunagerman/Desktop/Programming/Python/TTD/chromedriver'

class FunctionalTestCase(TestCase):

    # Opens browser    
    def setUp(self):
        self.browser = webdriver.Chrome(PATH)

    # Checks whether a certain word is in the page
    def test_there_is_homepage(self):
        self.browser.get('http://localhost:8000/')
        self.assertIn('Enter hash here:', self.browser.page_source)

    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000/')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        self.browser.find_element_by_name('submit').click()
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',self.browser.page_source)

    def test_hash_ajax(self):
        self.browser.get('http://localhost:8000/')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        time.sleep(5) # Wait for AJAX
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',self.browser.page_source)

    # Closes browser
    def tearDown(self):
        self.browser.quit()    

class UnitTestCase(TestCase):

    # Tests whether homepage exists
    def test_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')
    
    # Tests whether form exists and that it is valid
    def test_hash_form(self):
        form = HashForm(data={'text':'hello'})
        self.assertTrue(form.is_valid())
    
    def test_hash_func_works(self):
        text_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', text_hash)

    def save_Hash(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        hash.save()
        return hash

    # Ensuring inputed data and data in DB match
    def test_hash_object(self):
        hash = self.save_Hash()
        pulled_hash = Hash.objects.get(hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertEqual(hash.text, pulled_hash.text)

    # If we go to this site, we will see the text 'hello' - hash meaning
    def test_viewing_hash(self):
        hash = self.save_Hash()
        response = self.client.get('/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertContains(response, 'hello')

    def test_bad_data(self):
        def bad_hash():
            hash = Hash()
            hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824 **badinput**'
            hash.full_clean()
            self.assertRaises(ValidationError, bad_hash)

