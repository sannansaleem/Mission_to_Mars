#!/usr/bin/env python
# coding: utf-8

# In[1]:


#10.3.3 Scrape Mars Data: The News
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


#This is the path to the executable file we'll be using to automate our browser. This line isn't vital to our code
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html,'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find("div",class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
#For example, if we were to use .find_all() instead of .find() when pulling the summary, 
#we would retrieve all of the summaries on the page instead of just the first one.
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


#Instead of scraping each row, or the data in each <td />, we're going to scrape 
#the entire table with Pandas' .read_html() function.

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[15]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[16]:


df.to_html()


# # D1: Scrape High-Resolution Mars??? Hemisphere Images and Titles

# ### Hemispheres

# In[17]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[18]:


# Parse the data
hemi_html = browser.html
hemi_soup = soup(hemi_html, 'html.parser')

# Retrieve all items for hemispheres information
items = hemi_soup.find_all('div', class_='item')


# In[19]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[20]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.

main_url = "https://astrogeology.usgs.gov/"

# Create loop to scrape through all hemisphere information
for x in items:
    hemisphere = {}
    titles = x.find('h3').text
    # create link for full image
    link_ref = x.find('a', class_='itemLink product-item')['href']
    # Use the base URL to create an absolute URL and browser visit
    browser.visit(main_url + link_ref)
    # parse the data
    image_html = browser.html
    image_soup = soup(image_html, 'html.parser')
    download = image_soup.find('div', class_= 'downloads')
    img_url = download.find('a')['href']
    
    print(titles)
    print(img_url)
    
    # append list
    hemisphere['img_url'] = img_url
    hemisphere['title'] = titles
    hemisphere_image_urls.append(hemisphere)
    browser.back()


# In[21]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[22]:


# 5. Quit the browser
browser.quit()


# In[ ]:




