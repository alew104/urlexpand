from django.db import models
import requests
import bs4
from selenium import webdriver
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from mysite import settings

class Url(models.Model):
    origin = models.URLField()
    destination = models.URLField()
    httpstatus = models.IntegerField()
    title = models.TextField(max_length=200)
    pic = models.URLField(blank=True, null=True)
    imgname = models.TextField(blank=True, null=True)

    def create(self):
        r = requests.get(self.origin)
        self.destination = r.url
        self.httpstatus = r.status_code
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        self.title = soup.title.string
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        driver.get(r.url)
        temp = soup.title.string
        imgname = temp.lower()
        imgname = imgname.replace(" ", "")
        driver.save_screenshot('/tmp/' + imgname + '.png')
        driver.close()

        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        key = Key(bucket)
        key.key = '/img/' + imgname + '.png'
        key.set_contents_from_filename('/tmp/' + imgname + '.png')
        bucket.set_acl('public-read', '/img/' + imgname + '.png')
        os.remove('/tmp/' + imgname + '.png')
        self.pic = "https://s3-us-west-2.amazonaws.com/alew104-bucket/img/" + imgname + '.png'
        self.imgname = imgname
        self.save()


    def newimage(self):
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        imgname = self.imgname
        key = Key(bucket)
        key.key = '/img/' + imgname + '.png'
        bucket.delete_key(key)

        r = requests.get(self.destination)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        driver.get(r.url)
        temp = soup.title.string
        imgname = temp.lower()
        imgname = imgname.replace(" ", "")
        driver.save_screenshot('/tmp/' + imgname + '.png')
        self.imgname = imgname
        driver.close()

        key.set_contents_from_filename('/tmp/' + imgname + '.png')
        bucket.set_acl('public-read', '/img/' + imgname + '.png')
        os.remove('/tmp/' + imgname + '.png')
        url.pic = "https://s3-us-west-2.amazonaws.com/alew104-bucket/img/" + imgname + '.png'
        url.save()


    def delete(self, using=None):
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        imgname = self.imgname
        key = Key(bucket)
        key.key = '/img/' + imgname + '.png'
        bucket.delete_key(key)
        super(Url, self).delete()

    def __str__(self):
        return self.origin
