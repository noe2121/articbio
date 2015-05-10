from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import *
from lxml import etree
from appcore.models import *
import os
import os.path

# Create your views here.

def home(request):
	
	return render_to_response('index.html')

def subir_articulo(request):
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			doc = Archivo(archivo = request.FILES['archivo'])
			doc.save(form)
			print doc.archivo.path #Aqui se guarda el path de lo que acabamos de subir

			def Titulo(direccion): #obtiene el titulo
				xml = etree.parse(direccion)
				tag = xml.getroot()
				primer_elemento= tag[0]
				titulo = primer_elemento.find("Article/ArticleTitle")# son los tags donde esta el titulo

				if titulo.text == None:
					return render_to_response('cargado_incorrecto.html')

				return titulo.text

			def Abstract(direccion): #obtiene el abstract
				xml = etree.parse(direccion)
				tag = xml.getroot()
				primer_elemento= tag[0]
				abstract = primer_elemento.find("Article/Abstract/AbstractText")

				if abstract.text == None:
					return render_to_response('cargado_incorrecto.html')

				return abstract.text

			def Autor(direccion):#obtiene el autor
				xml = etree.parse(direccion)
				tag = xml.getroot()
				primer_elemento= tag[0]
				lastName = primer_elemento.find("Article/AuthorList/Author/LastName")
				ForeName = primer_elemento.find("Article/AuthorList/Author/ForeName")

				if lastName == None and ForeName == None:
					nombre = "N/A"
					return nombre
				elif lastName.text == None and ForeName.text == None:
					nombre = "N/A"
					return nombre

				nombre = lastName.text + " " + ForeName.text #concatene esta parte para que fuera el apeido y nombre 
				return nombre
		
			def Fecha(direccion):#obtiene la fecha
				xml = etree.parse(direccion)
				tag = xml.getroot()
				primer_elemento= tag[1]
				year = primer_elemento.find("History/PubMedPubDate/Year").text
				month = primer_elemento.find("History/PubMedPubDate/Month").text
				day = primer_elemento.find("History/PubMedPubDate/Day").text

				if year == None:
					year = "2000"

				if month == None:
					month = "01"

				if day == None:
					day = "01"

				fecha = year + "-" + month + "-" + day # en la parte de la fecha la concatene para que saliera del tipo dd/mm/yyyy
				return fecha
		
			def Revista(direccion):#obtiene la revista
				xml = etree.parse(direccion)
				tag = xml.getroot()
				primer_elemento= tag[0]
				revista = primer_elemento.find("Article/Journal/Title")
				if revista == None:
					revista = "N/A"
					return revista
				elif revista.text == None:
					revista = "N/A"
					return revista

				return revista.text

			def Palabras_clave(direccion):#obtiene la revista
				xml = etree.parse(direccion)
				tag = xml.getroot()
				primer_elemento= tag[0]
				palabras_clave = primer_elemento.find("KeywordList/Keyword")
				if palabras_clave == None:
					palabras_clave = "N/A"
					return palabras_clave
				elif palabras_clave.text == None:
					palabras_clave = "N/A"
					return palabras_clave

				return palabras_clave.text

			def Editorial(direccion):#obtiene la revista
				xml = etree.parse(direccion)
				tag = xml.getroot()
				primer_elemento= tag[0]
				editorial = primer_elemento.find("Article/Editorial")
				if editorial == None:
					editorial = "N/A"
					return editorial
				elif editorial.text == None:
					editorial = "N/A"
					return editorial

				return editorial.text

			def Paginas(direccion):#obtiene la revista
				xml = etree.parse(direccion)
				tag = xml.getroot()
				primer_elemento= tag[0]
				paginas = primer_elemento.find("Article/Pagination/MedlinePgn")
				if paginas == None:
					paginas = "N/A"
					return paginas
				elif paginas.text == None:
					paginas = "N/A"
					return paginas

				return paginas.text
		
			def DOI(direccion):#obtiene el DOi
				xml = etree.parse(direccion)
				tag = xml.getroot()
				primer_elemento= tag[1]
				doi = primer_elemento.find("ArticleIdList/ArticleId")
				if doi == None:
					doi = "N/A"
					return doi
				elif doi.text == None:
					doi = "N/A"
					return doi
					
				return doi.text

			def Url(direccion):#obtiene el DOi
				xml = etree.parse(direccion)
				tag = xml.getroot()
				primer_elemento= tag[1]
				url = primer_elemento.find("Url")
				if url == None:
					url = "N/A"
					return url
				elif url.text == None:
					url = "N/A"
					return url

				return url.text
		
			class xml:
				def __init__(self,direccion):
					self.titulo = Titulo(direccion)
					self.abstract = Abstract(direccion)
					self.autor = Autor(direccion)
					self.fecha = Fecha(direccion)
					self.revista = Revista(direccion)
					self.palabras_clave = Palabras_clave(direccion)
					self.editorial = Editorial(direccion)
					self.paginas = Paginas(direccion)
					self.DOI = DOI(direccion)
					self.url = Url(direccion)
		
			objeto = xml(doc.archivo.path)
			os.remove(doc.archivo.path)
		
			art = Articulo()
			art.titulo = objeto.titulo
			art.abstract = objeto.abstract
			art.autor = objeto.autor
			art.fecha = objeto.fecha
			art.revista = objeto.revista
			art.palabras_clave = objeto.palabras_clave
			art.editorial = objeto.editorial
			art.paginas = objeto.paginas
			art.doi = objeto.DOI
			art.url = objeto.url
		
			art.save()
		
		
			t = get_template("upload_correcto.html")
			c = Context({'titulo':objeto.titulo, 'abstract':objeto.abstract, 'autor':objeto.autor, 'fecha':objeto.fecha, 'revista':objeto.revista, 'palabras_clave':objeto.palabras_clave, 'editorial':objeto.editorial, 'paginas':objeto.paginas, 'doi':objeto.DOI, 'url':objeto.url})
			html = t.render(c)

			return HttpResponse(html)
	else:
		form = UploadForm()
	return render(request, 'subir.html', {'form': form})


def capturar_articulo(request):
	if request.method == 'POST':
		form = FormularioArticulo(request.POST)
		if form.is_valid():

			art = Articulo()

			art.titulo = form.cleaned_data['titulo']
			art.abstract = form.cleaned_data['abstract']
			art.autor = form.cleaned_data['autor']
			art.fecha = form.cleaned_data['fecha']
			art.editorial = form.cleaned_data['editorial']
			art.revista = form.cleaned_data['revista']
			art.paginas = form.cleaned_data['paginas']
			art.doi = form.cleaned_data['doi']
			art.url = form.cleaned_data['url']
			art.palabras_clave = form.cleaned_data['palabras_clave']

			art.save()

			return render_to_response('cargado_correcto.html')

	else:
		form = FormularioArticulo()

	return render(request, 'capturar_articulo.html', {'form':form})


def busquedas(request):
	if request.method == 'POST':
		form_titulo = BusquedaTituloForm(request.POST)
		form_abstract = BusquedaAbstractForm(request.POST)
		form_autor = BusquedaAutorForm(request.POST)
		form_fecha = BusquedaFechaForm(request.POST)
		form_editorial = BusquedaEditorialForm(request.POST)
		form_revista = BusquedaRevistaForm(request.POST)
		form_doi = BusquedaDoiForm(request.POST)
		form_palabras_clave = BusquedaPalabrasClaveForm(request.POST)

		#TITULO
		if form_titulo.is_valid():

			filtro = form_titulo.cleaned_data['busqueda_por_titulo']
			filtrado = Articulo.objects.filter(titulo__contains = filtro)

			t = get_template("muestra_articulos.html")
			c = Context({'filtrado': filtrado})
			html = t.render(c)

			return HttpResponse(html)

		#ABSTRACT
		if form_abstract.is_valid():

			filtro = form_abstract.cleaned_data['busqueda_por_abstract']
			filtrado = Articulo.objects.filter(abstract__contains = filtro)

			t = get_template("muestra_articulos.html")
			c = Context({'filtrado': filtrado})
			html = t.render(c)

			return HttpResponse(html)

		#AUTOR
		if form_autor.is_valid():

			filtro = form_autor.cleaned_data['busqueda_por_autor']
			filtrado = Articulo.objects.filter(autor__contains = filtro)

			t = get_template("muestra_articulos.html")
			c = Context({'filtrado': filtrado})
			html = t.render(c)

			return HttpResponse(html)

		#FECHA
		if form_fecha.is_valid():

			filtro = form_fecha.cleaned_data['busqueda_por_fecha']
			filtrado = Articulo.objects.filter(fecha__contains = filtro)

			t = get_template("muestra_articulos.html")
			c = Context({'filtrado': filtrado})
			html = t.render(c)

			return HttpResponse(html)

		#EDITORIAL
		if form_editorial.is_valid():

			filtro = form_editorial.cleaned_data['busqueda_por_editorial']
			filtrado = Articulo.objects.filter(editorial__contains = filtro)

			t = get_template("muestra_articulos.html")
			c = Context({'filtrado': filtrado})
			html = t.render(c)

			return HttpResponse(html)

		#REVISTA
		if form_revista.is_valid():

			filtro = form_revista.cleaned_data['busqueda_por_revista']
			filtrado = Articulo.objects.filter(revista__contains = filtro)

			t = get_template("muestra_articulos.html")
			c = Context({'filtrado': filtrado})
			html = t.render(c)

			return HttpResponse(html)

		#DOI
		if form_doi.is_valid():

			filtro = form_doi.cleaned_data['busqueda_por_doi']
			filtrado = Articulo.objects.filter(doi__contains = filtro)

			t = get_template("muestra_articulos.html")
			c = Context({'filtrado': filtrado})
			html = t.render(c)

			return HttpResponse(html)

		#PALBRAS CLAVE
		if form_palabras_clave.is_valid():

			filtro = form_palabras_clave.cleaned_data['busqueda_por_palabras_clave']
			filtrado = Articulo.objects.filter(palabras_clave__contains = filtro)

			t = get_template("muestra_articulos.html")
			c = Context({'filtrado': filtrado})
			html = t.render(c)

			return HttpResponse(html)

	else:
		form_titulo = BusquedaTituloForm()
		form_abstract = BusquedaAbstractForm()
		form_autor = BusquedaAutorForm()
		form_fecha = BusquedaFechaForm()
		form_editorial = BusquedaEditorialForm()
		form_revista = BusquedaRevistaForm()
		form_doi = BusquedaDoiForm()
		form_palabras_clave = BusquedaPalabrasClaveForm()

	return render(request, 'busquedas.html', {'form_titulo':form_titulo, 'form_abstract':form_abstract, 'form_autor':form_autor, 'form_fecha':form_fecha, 'form_revista':form_revista, 'form_editorial':form_editorial, 'form_doi':form_doi, 'form_palabras_clave':form_palabras_clave})


def mostrar_articulo_por_id(request, id_num):

	objeto = Articulo.objects.get(id = id_num)
		
	t = get_template("solo_muestra.html")
	c = Context({'titulo':objeto.titulo, 'abstract':objeto.abstract, 'autor':objeto.autor, 'fecha':objeto.fecha, 'revista':objeto.revista, 'palabras_clave':objeto.palabras_clave, 'editorial':objeto.editorial, 'paginas':objeto.paginas, 'doi':objeto.doi, 'url':objeto.url})
	html = t.render(c)

	return HttpResponse(html)

def mostrar_todos_eliminar(request):

	filtrado = Articulo.objects.all()

	t = get_template("lista_todos.html")
	c = Context({'filtrado': filtrado})
	html = t.render(c)

	return HttpResponse(html)

def eliminar_por_id(request, id_eliminar_por_id):
	
	objeto = Articulo.objects.get(id=id_eliminar_por_id)
	
	objeto.delete()
	
	return render_to_response('eliminar_correcto.html')