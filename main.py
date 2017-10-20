import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

ACCESS_TOKEN = '6237175266.3c426f2.3fca7d5581864fbcb3cfa347ce8221cc'
BASE_URL = 'https://api.instagram.com/v1/'


def self_info():
    end_point = 'users/self/'
    request_url = (BASE_URL + end_point + '?access_token=%s') % ACCESS_TOKEN
    user_info = requests.get(request_url).json()
    print 'GET request url : %s' % request_url

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Error Occurred. Try after sometime.'


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Error Occurred. Try after sometime.'
        exit()


def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % {user_id, ACCESS_TOKEN}
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Error Occurred. Try after sometime.'


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % ACCESS_TOKEN
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            return own_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Error Occurred. Try after sometime.'
    return None


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            return user_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Error Occurred. Try after sometime.'
    return None


def like_a_post(insta_username):
    media_id = get_user_post(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like['meta']['code'] == 200:
        print 'Liked.'
    else:
        print 'Error Occurred. Try after sometime.'


def post_a_comment(insta_username):
    media_id = get_user_post(insta_username)
    comment_text = raw_input("\nEnter Your Comment Here: \t")

    if len(comment_text) < 250:
        payload = {"access_token": ACCESS_TOKEN, "text": comment_text}
        comment_url = (BASE_URL + 'media/%s/comments') % media_id
        make_comment = requests.post(comment_url, payload).json()

        if make_comment['meta']['code'] == 200:
            print "Comment posted Successfully!"
        else:
            print "Comment Unsuccessful."
    else:
        print "Comment should be only 250 letters long"

def delete_negative_comment(insta_username):
    media_id = get_user_post(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            comment_text = comment_info['data'][0]['text']
            comment_id = comment_info['data']['id']
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
            if blob.sentiment['classification'] == 'NEG':
                request_url = (BASE_URL + 'media/%s/comments/%s?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                comment_result = requests.get(request_url).json()
                if comment_info['meta']['code'] == 200:
                    print "Comment deleted Successfully!"
                else:
                    print "Comment deletion Unsuccessful."
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Error Occurred. Try after sometime.'


# self_info()
#insta_username = str(raw_input("Enter username you want to search : "))
insta_username = 'acadviewtest'
delete_negative_comment(insta_username)
