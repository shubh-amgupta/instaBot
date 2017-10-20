import requests

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
        print 'Error Occured. Try after sometime.'


self_info()
