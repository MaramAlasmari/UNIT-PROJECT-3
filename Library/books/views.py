from django.shortcuts import render,redirect
from django.http import HttpRequest
from .models import Book, Review


# Create your views here.
def add_book_view(request: HttpRequest):

    msg = None
    if request.method == "POST":
        try:
            new_book = Book(name=request.POST["name"], brief=request.POST["brief"], writer=request.POST["writer"], release_date=request.POST["release_date"], publishing_house=request.POST["publishing_house"], category=request.POST["category"],content=request.FILES["content"])
            
            if "poster" in request.FILES:
                new_book.poster = request.FILES["poster"]

            new_book.save()
            return redirect("books:book_home")
        except Exception as e:
            msg = f"An error occured, please fill in all fields and try again . {e}"
       
    return render(request, "books/add.html", {"categories" : Book.categories,"msg" : msg})


def book_home(request: HttpRequest):

    books = Book.objects.all()

    return render(request, "books/book_home.html", {"books" : books})



def book_detail_view(request:HttpRequest,book_id):

    book_detail = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book= book_detail)
   

    return render(request, "books/book_detail.html", {"book" : book_detail, "reviews" : reviews})



def search(request: HttpRequest):
    if 'search' in request.GET:
        query = request.GET['search']
        books = Book.objects.filter(name__contains=query)
    else:
         books = Book.objects.all()   
    return render(request, 'books/search.html',  {"books" : books})



def delete(request: HttpRequest, book_id):
  

    book = Book.objects.get(id=book_id)
    book.delete()

    return redirect("books:book_home")


    #if not request.user.is_staff:
        #return render(request, status=401)

def update(request : HttpRequest,book_id):


    
    book=Book.objects.get(id=book_id)
    
    if request.method=="POST":
        book.name=request.POST['name']
        book.brief=request.POST["brief"]
        book.writer=request.POST["writer"]
        book.release_date=request.POST["release_date"]
        book.publishing_house=request.POST["publishing_house"]

        book.save()
       
        return redirect('books:book_detail_view',book_id=book.id)
    
    return render(request,'books/update.html',{"book" : book,'categories':Book.categories})



def add_review_view(request: HttpRequest, book_id):

    if request.method == "POST":

        if not request.user.is_authenticated:
            return render(request, status=401)

        book_rev = Book.objects.get(id=book_id)
        new_review = Review(book=book_rev, user=request.user, rating=request.POST["rating"], comment=request.POST["comment"])  
        new_review.save()
        return redirect("books:book_detail_view", book_id=book_rev.id)
    

def bookCat(request : HttpRequest):

    if "category" in request.GET and request.GET["category"] =="literature":
      books = Book.objects.filter(category__contains ="literature")

    elif "category" in request.GET and request.GET["category"] =="philosophy":
        books = Book.objects.filter(category__contains ="philosophy")

    elif "category" in request.GET and request.GET["category"] =="novel":
        books = Book.objects.filter(category__contains ="novel")

    elif "category" in request.GET and request.GET["category"] =="psychic":
        books = Book.objects.filter(category__contains ="psychic")

    elif "category" in request.GET and request.GET["category"] =="sciences":
        books = Book.objects.filter(category__contains ="sciences")    
    else:
        books = Book.objects.all()
    return render(request ,"books/book_home.html" , {"books" : books})
