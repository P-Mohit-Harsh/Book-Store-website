from django.shortcuts import render
from django.http import HttpResponse
from .models import books
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Create your views here.
def home(request):    
    
    popular_books=[]
    
    df = pd.read_csv('main_dataset.csv')
    df.dropna(inplace=True)
    
    for i in df[(df['name'].str.len()<=20) & (df['book_depository_stars']>=4)].sample(4).values:
        
        obj = books()
        obj.title = i[1]
        obj.author = i[2]
        obj.price = i[7]
        obj.cap = ','.join(list(i[9].split('-'))[:3])
        obj.img = i[10]
        
        if(i[4]==5):
            obj.stars = "star rating/5star.jpg"
        elif(i[4]>4):
            obj.stars = "star rating/4.5star.jpg"
        elif(i[4]==4):
            obj.stars = "star rating/4star.jpg"
        else:
            obj.stars = "star rating/3.5star.jpg"
        
        popular_books.append(obj)
    
    new_books = []
    
    for i in df[df['name'].str.len()<=20].tail(30).sample(4).values:
        
        obj = books()
        obj.title = i[1]
        obj.author = i[2]
        obj.price = i[7]
        obj.cap = ','.join(list(i[9].split('-')))
        obj.img = i[10]
        
        if(i[4]==5):
            obj.stars = "star rating/5star.jpg"
        elif(i[4]>4):
            obj.stars = "star rating/4.5star.jpg"
        elif(i[4]==4):
            obj.stars = "star rating/4star.jpg"
        else:
            obj.stars = "star rating/3.5star.jpg"
        
        new_books.append(obj)
        
    deal_books = []
    
    best_books = []
        
    for i in df[(df['name'].str.len()<=20) & (df['old_price']<=5)].sample(4).values:
        
        obj = books()
        obj.title = i[1]
        obj.author = i[2]
        obj.price = i[7]
        obj.cap = ','.join(list(i[9].split('-')))
        obj.img = i[10]
        
        if(i[4]==5):
            obj.stars = "star rating/5star.jpg"
        elif(i[4]>4):
            obj.stars = "star rating/4.5star.jpg"
        elif(i[4]==4):
            obj.stars = "star rating/4star.jpg"
        else:
            obj.stars = "star rating/3.5star.jpg"
        
        deal_books.append(obj)
        
    for i in df[(df['name'].str.len()<=20) & (df['book_depository_stars']>=4) & (df['old_price']<=6)].sample(4).values:
        
        obj = books()
        obj.title = i[1]
        obj.author = i[2]
        obj.price = i[7]
        obj.cap = ','.join(list(i[9].split('-')))
        obj.img = i[10]
        
        if(i[4]==5):
            obj.stars = "star rating/5star.jpg"
        elif(i[4]>4):
            obj.stars = "star rating/4.5star.jpg"
        elif(i[4]==4):
            obj.stars = "star rating/4star.jpg"
        else:
            obj.stars = "star rating/3.5star.jpg"
        
        best_books.append(obj)
    
    return render(request, 'home.html',{'popular_books': popular_books,'new_books':new_books,'deal_books':deal_books,'best_books':best_books})

def search(request):
    
    df = pd.read_csv('main_dataset.csv')
    df.dropna(inplace=True)
    
    df.drop(['format','currency','isbn','price'],axis=1,inplace=True)
    
    mod_names = []
    for i in df['name']:
        x = [a for a in i.lower() if a not in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~']
        mod_names.append(''.join(x))
    df['mod_names'] = mod_names
    
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(df['mod_names'])
    
    query = request.GET['book_name']
    processed = re.sub("[^a-zA-Z0-9 ]", "", query.lower())
    query_vec = vectorizer.transform([processed])
    similarity = cosine_similarity(tfidf,query_vec).flatten()
    indices = np.argpartition(similarity, -50)[-50:]
    results = df.iloc[indices]
    results = results.iloc[::-1]
      
    searched_books=[]
    k=0
    
    for i in range(5):
        
        books_list = []
        
        for j in range(4):
            
            obj = books()
            obj.title = results.iloc[k][1]
            obj.author = results.iloc[k][2]
            obj.cap = ','.join(list(results.iloc[k][5].split('-'))[:3])
            obj.price = results.iloc[k][4]
            obj.img = results.iloc[k][6]
            
            if(results.iloc[k][3]==5):
                obj.stars = "star rating/5star.jpg"
            elif(results.iloc[k][3]>4):
                obj.stars = "star rating/4.5star.jpg"
            elif(results.iloc[k][3]==4):
                obj.stars = "star rating/4star.jpg"
            else:
                obj.stars = "star rating/3.5star.jpg"
            
            books_list.append(obj)
            
            k+=1

        searched_books.append(books_list)
    
    return render(request, 'search_page.html', {'searched_books':searched_books})