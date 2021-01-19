from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.db.models import Avg

from .models import Book, authorsToString, Review

import requests
import re

# Create your views here.
def home(request):
    return render(request, "home/search.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def search(request):
    if request.method == "GET":
        q = request.GET["search_term"]
        url = f"https://www.googleapis.com/books/v1/volumes?q={q}"
        res = requests.get(url)
        data = res.json()
        booksFound = data["items"]

        searchResults = []

        for i in range(len(booksFound)):

            defaultCover = "https://islandpress.org/sites/default/files/default_book_cover_2015.jpg"
            imgUrl = booksFound[i]["volumeInfo"].get("imageLinks")
            if imgUrl is None:
                imgUrl = defaultCover
            else:
                imgUrl = imgUrl.get("smallThumbnail", defaultCover)

            bookDict = {
                "title" : booksFound[i]["volumeInfo"]["title"],
                "authors" : authorsToString(booksFound[i]["volumeInfo"].get("authors", "unknown")),
                "imgUrl" : imgUrl,
                "summary" : booksFound[i]["volumeInfo"].get("description"),
                "id" : booksFound[i]["id"]
            }
            book = Book(bookDict)
            searchResults.append(book)


        return render(request, "home/results.html", {
            "results" : searchResults,
            "numResults" : len(searchResults),
        })
    else:
        return render(request, "home/search.html")

def results_view(request):
    return render(request, "home/results.html")


def book_page_view(request, bookId):

    # display books data without database dependencies
    url = f"https://www.googleapis.com/books/v1/volumes/{bookId}"
    res = requests.get(url)
    data = res.json()
    book = data

    description = book["volumeInfo"].get("description", "Sorry! This book does not have a description yet!")
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', description)

    bookDict = {
        "title" : book["volumeInfo"]["title"],
        "authors" : authorsToString(book["volumeInfo"]["authors"]),
        "imgUrl" : book["volumeInfo"]["imageLinks"]["smallThumbnail"],
        "summary" : cleantext,
        "id" : book["id"]
    }

    book = Book(bookDict)

    #handle books ratings and reviews
    reviews = Review.objects.filter(book_id=book.id)
    if not reviews:
        message = "No reviews have been submitted. Write the first review?"
        rating = ""
    else:
        message = ""
        rating = reviews.aggregate(Avg('rating'))

    return render(request, "home/book_page.html", {
        "book" : book,
        "message" : message,
        "rating" : rating
    })