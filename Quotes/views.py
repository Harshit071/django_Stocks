from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django .contrib import messages

def home(request):
	import requests
	import json

	if request.method == "POST":
		ticker=request.POST['ticker']
		api_request=requests.get("https://api.iex.cloud/v1/data/core/quote/" + ticker +"?token=sk_463b8bbc111b4011b22ef6e77af7c043")

		try:
			api=json.loads(api_request.content)

		except Exception as e:
			api="Error"

		return render(request, 'home.html' , {'api':api})


	else:

		return render(request, 'home.html' , {'ticker':"Enter a ticker  Above.."})


def about(request):
	return render(request,'about.html',{})



def add_stock(request):
	import requests
	import json

	if request.method == "POST":
		form=StockForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request,('Stock has been added'))
			return redirect("add_stock")



	else:

		ticker=Stock.objects.all()
		output=[]
		for ticker_item in ticker:
			api_request=requests.get("https://api.iex.cloud/v1/data/core/quote/" + str(ticker_item) +"?token=sk_463b8bbc111b4011b22ef6e77af7c043")

			try:
				api=json.loads(api_request.content)
				output.append(api)

			except Exception as e:
				api="Error"

		return render(request,'add_stock.html',{'ticker':ticker,'output':output})

 


def delete(request,stock_id):

	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request,("Stock has been deleted"))
	return redirect(Delete_Stock)


def Delete_Stock(request):
	ticker=Stock.objects.all()
	return render(request,'Delete_Stock.html',{'ticker':ticker})