import unittest

from django.test.client import Client
from django.contrib.sites.models import Site
from django.conf import settings

from cms.api import create_page
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from cms_redirects.models import CMSRedirect

class TestRedirects(unittest.TestCase):
    def setUp(self):
        settings.APPEND_SLASH = False

        self.site = Site.objects.get_current()
        self.page = create_page(
            title="Hello world!",
            template=TEMPLATE_INHERITANCE_MAGIC,
            language='en',
            site=self.site,
            published=True,
        )
        self.page.set_as_homepage()

    def test_301_page_redirect(self):
        r_301_page = CMSRedirect(site=self.site, page=self.page, old_path='/301_page.php')
        r_301_page.save()

        c = Client()
        r = c.get('/301_page.php')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r['location'], '/')

    def test_302_page_redirect(self):
        r_302_page = CMSRedirect(site=self.site, page=self.page, old_path='/302_page.php', response_code='302')
        r_302_page.save()

        c = Client()
        r = c.get('/302_page.php')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r['location'], '/')

    def test_301_path_redirect(self):
        r_301_path = CMSRedirect(site=self.site, new_path='/', old_path='/301_path.php')
        r_301_path.save()

        c = Client()
        r = c.get('/301_path.php')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r['location'], '/')

    def test_302_path_redirect(self):
        r_302_path = CMSRedirect(site=self.site, new_path='/', old_path='/302_path.php', response_code='302')
        r_302_path.save()

        c = Client()
        r = c.get('/302_path.php')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r['location'], '/')

    def test_410_redirect(self):
        r_410 = CMSRedirect(site=self.site, old_path='/410.php', response_code='302')
        r_410.save()

        c = Client()
        r = c.get('/410.php')
        self.assertEqual(r.status_code, 410)

    def test_redirect_can_ignore_query_string(self):
        """
        Set up a redirect as in the generic 301 page case, but then try to get this page with
        a query string appended.  Succeed nonetheless.
        """
        r_301_page = CMSRedirect(site=self.site, page=self.page, old_path='/301_page_with_qs.php')
        r_301_page.save()

        c = Client()
        r = c.get('/301_page_with_qs.php?this=is&a=query&string')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r['location'], '/')
