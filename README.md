# fbpagepost
Python post to Facebook page guide using GraphAPI

In this post, you will learn how to post to a Facebook page's wall (acting as the page) using Python. It includes step by step instructions to create a new page, register an app with Facebook and some python code.

Step 1

First, create a new Facebook page. Select appropriate page type, fill in description and other relevant fields.
On the new page, go to About tab, and note the Facebook Page ID.
We will post to this page's wall, acting as the page.
Step 2

Now create a Facebook App which will be used to access Facebook's Graph API.
Go to Facebook Apps dashboard -> Click '+ Add a New App' -> Create a New App ID - Choose a new Display Name for your app ->
Go to Facebook Apps dashboard, Get Started with the Facebook SDK
Click 'Choose Platform'-> Select a platform to get started -> Choose platform WWW -> Click on 'Skip quick start'
Go to APP Review -> Make <YOUR_APP_NAME> public? -> Toggle the button to Yes -> Make App Public? -> Yes. This will enable others to see posts by your app in their timelines - otherwise, only you will see the wall posts by the app.
Now - you should see a green dot next to app's name and Approved items, and the text 'Your app is currently live and available to the public'.
Make a note of the App ID and App Secret (Click Show next to it; you will be asked to re-enter your Facebook password).
Step 3

In this step we will obtain obtain Facebook OAuth token. A long-lived token at that! Read about Facebook access tokens.
Go to Graph API Explorer -> In the Application drop down -> Select the app created in Step 2 -> Click Get Page Access Token -> In Permissions popup go to Extended Permissions tab -> Select manage_pages, and publish_actions These permissions will allow your app to publish posts acting as the page -> Click Get Access Token -> You will see a message saying "{App} would like to post publicly to Facebook for you. Who do you want to share these posts with?" -> I chose Public for maximum visibility - as I wanted to post to a public page.
You might be asked to Turn On Platform if you disabled it previously, enable it! If you mess this step up, just go to your App Settings - remove the app and try again.
Make a note of the short-lived token shown in Graph API Explorer.
Facebook has deprecated offline access, the next best thing is long-lived token which expires in 60 days. We will convert the short-lived access token noted above to a long-lived token. 
 In order to extend the access token you need to make the following request with your short lived access token:

https://graph.facebook.com/oauth/access_token?             
    client_id=APP_ID&
    client_secret=APP_SECRET&
    grant_type=fb_exchange_token&
    fb_exchange_token=EXISTING_ACCESS_TOKEN 
You should see access_token={...}&expires={...}. This new access_token is the long-lived token we will use in our Python script.
{"access_token":"","token_type":"bearer","expires_in":""}
long-lived token will also expire eventually, be prepared to perform this Step 3 again before that happens! If you do not want to deal with that just save the page_access_tokencomputed in Step 4 - and you can use it forever, as according to Facebook's documentation a page access token obtained from long-lived user token will not have any expiry time.
Step 4

We will use Facebook Python SDK to access Facebook's Graph API. You can install it using pip: pip install facebook-sdk (again, use of virtualenv is highly recommended).
Finally, this python script will post to Facebook page's wall:

import facebook

def main():
  # Fill in the values noted in previous steps here
  cfg = {
    "page_id"      : "VALUE",  # Step 1
    "access_token" : "VALUE"   # Step 3
    }

  api = get_api(cfg)
  msg = "Hello, world!"
  status = api.put_wall_post(msg)

def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  # Get page token to post as the page. You can skip 
  # the following if you want to post as yourself. 
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

if __name__ == "__main__":
  main()
Good to go!

Next steps

Allow multiple people to log-in to the app? I am not sure how to exactly do it, but here are a few pointers:

First step would be to add a login dialogue - instead of Step 3. This will be a popup from facebook.com which will show which permissions your app is requesting.
The 'login' API call will return a short-lived token. This is the tricky part, user is viewing a facebook.com page right now, how will your app get the auth token? Might be easier to do using their Javascript login flow. Other option is to give a redirect URL - which will be called when the popup is closed (and token added as a parameter).
Once you get the short-lived token, you can follow the tutorial - convert to long-livedand store that in a database - sqlite3 works very well for small prototypes.
Read these two links to understand more: Facebook.com - Manual login flow, Facebook.com Web login flow (javascript).
If required, renew the long-lived token for your users.
