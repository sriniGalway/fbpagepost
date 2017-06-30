#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:59:08 2017

@author: Srinivasan Arumugam
"""

import facebook

def main():
  cfg = {
    "page_id"      : "ENTER PAGE ID",  # Step 1
    "access_token" : "ENTER ACCESS TOKEN"   # Step 3
    }
    
#  https://graph.facebook.com/oauth/access_token?             
#        client_id=APP_ID&
#        client_secret=SECRET_ID&
#        grant_type=fb_exchange_token&
#        fb_exchange_token=SHORT_TIME_ACCESS_TOKEN

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