import requests #Import to make http requests
import urllib #Import to download images from url
from textblob import TextBlob #Import to analyse text
from textblob.sentiments import NaiveBayesAnalyzer

ACCESS_TOKEN = '6237175266.3c426f2.3fca7d5581864fbcb3cfa347ce8221cc' #access_token is like a key-card for your hotel room. to access api
BASE_URL = 'https://api.instagram.com/v1/' #base-url remains same for every request to api. End-points changes.


#funtion to fetch user's info
def self_info():
    end_point = 'users/self/'
    request_url = (BASE_URL + end_point + '?access_token=%s') % ACCESS_TOKEN
    user_info = requests.get(request_url).json()

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


#function to fetch user's id from username
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
    #print request_url
    user_info = requests.get(request_url).json()
    #print user_info
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Error Occurred. Try after sometime.'
        exit()


#function to fectch user's info from user's id from get_user_id function
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


#fetch user's recent funtion
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


#function to fetch users post from username
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


#function to like a post
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


#get list of users who have liked the post
def get_users_list(insta_username):
    media_id = get_user_post(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, ACCESS_TOKEN)
    users_info = requests.get(request_url).json()

    if users_info['meta']['code'] == 200:
        if len(users_info['data']):
            for user in users_info['data']:
                print 'Username: %s' % (users_info['data'][user]['username'])
        else:
            print 'User does not exist!'
    else:
        print 'Error Occurred. Try after sometime.'


#function to post a comment
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


#to delete a negative comment
def delete_negative_comment(insta_username):
    media_id = get_user_post(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            comment_text = comment_info['data'][0]['text']
            comment_id = comment_info['data'][0]['id']
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer()) #analyse comment if negative or positive
            if blob.sentiment[0] == 'neg':
                request_url = (BASE_URL + 'media/%s/comments/%s?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                comment_result = requests.delete(request_url).json() #delete a comment url
                if comment_result['meta']['code'] == 200:
                    print "Comment deleted Successfully!"
                else:
                    print "Comment deletion Unsuccessful."
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Error Occurred. Try after sometime.'


#delete multiple negative comments
def delete_all_negative_comment(insta_username):
    media_id = get_user_post(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for comment in comment_info['data']:
                comment_text = comment_info['data'][comment]['text']
                comment_id = comment_info['data'][comment]['id']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())  # analyse comment if negative or positive
                if blob.sentiment[0] == 'neg':
                    request_url = (BASE_URL + 'media/%s/comments/%s?access_token=%s') % (
                    media_id, comment_id, ACCESS_TOKEN)
                    comment_result = requests.delete(request_url).json()  # delete a comment url
                    if comment_result['meta']['code'] == 200:
                        print "Comment deleted Successfully!"
                    else:
                        print "Comment deletion Unsuccessful."
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Error Occurred. Try after sometime.'


#delete a comment with a particular word
def delete_comment_with_word(insta_username):
    media_id = get_user_post(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    comment_info = requests.get(request_url).json()
    word = str(raw_input("Enter a word you want to search for in comments to delete: "))

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for comment in comment_info['data']:
                comment_text = comment_info['data'][comment]['text']
                comment_id = comment_info['data']['id']

                if word in comment_text:
                    request_url = (BASE_URL + 'media/%s/comments/%s?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                    comment_result = requests.get(request_url).json() #delete a comment url
                    if comment_info['meta']['code'] == 200:
                        print "Comment deleted Successfully!"
                    else:
                        print "Comment deletion Unsuccessful."
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Error Occurred. Try after sometime.'



choice = True
while choice == True:
    print "Welcome to InstaBot\n"
    menu_choice = int(raw_input("Enter your choice:\n1. Get your own info.\n2. Get a user's info\n3. Get your posts.\n4. Get user's post.\n5. Like a post.\n6. Get user's list.\n7. Post a comment.\n8. Delete a negative comment.\n9. Delete all negative comments.\n10. Delete comment with a particular word.\n11. Exit \n"))

    if menu_choice == 1:
        self_info()
    elif menu_choice == 2:
        insta_username = raw_input("Enter username of user : ")
        get_user_info(insta_username)
    elif menu_choice == 3:
        get_own_post()
    elif menu_choice == 4:
        insta_username = raw_input("Enter username of user : ")
        get_user_post(insta_username)
    elif menu_choice == 5:
        insta_username = raw_input("Enter username of user : ")
        like_a_post(insta_username)
    elif menu_choice == 6:
        insta_username = raw_input("Enter username of user : ")
        get_users_list(insta_username)
    elif menu_choice == 7:
        insta_username = raw_input("Enter username of user : ")
        post_a_comment(insta_username)
    elif menu_choice == 8:
        insta_username = raw_input("Enter username of user : ")
        delete_negative_comment(insta_username)
    elif menu_choice == 9:
        insta_username = raw_input("Enter username of user : ")
        delete_all_negative_comment(insta_username)
    elif menu_choice == 10:
        insta_username = raw_input("Enter username of user : ")
        delete_comment_with_word(insta_username)
    else:
        choice = False

