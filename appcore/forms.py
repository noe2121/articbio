from django import forms

# Create your forms here.

class UploadForm(forms.Form):
	archivo = forms.FileField(label='Selecciona un articulo en xml')

class FormularioArticulo(forms.Form):

	titulo = forms.CharField(max_length = 100)
	abstract = forms.CharField(widget = forms.Textarea)
	autor = forms.CharField(max_length = 100)
	fecha = forms.DateField()
	editorial = forms.CharField(max_length = 50)
	revista = forms.CharField(max_length = 50)
	paginas = forms.CharField(max_length = 20)
	doi = forms.CharField(max_length = 100)
	url = forms.CharField(max_length = 200)
	palabras_clave = forms.CharField(max_length = 100)






class BusquedaTituloForm(forms.Form):

	busqueda_por_titulo = forms.CharField(max_length  = 100)

class BusquedaAbstractForm(forms.Form):

	busqueda_por_abstract = forms.CharField(max_length  = 100)

class BusquedaAutorForm(forms.Form):

	busqueda_por_autor = forms.CharField(max_length  = 100)

class BusquedaFechaForm(forms.Form):

	busqueda_por_fecha = forms.DateField()

class BusquedaEditorialForm(forms.Form):

	busqueda_por_editorial = forms.CharField(max_length  = 50)

class BusquedaDoiForm(forms.Form):

	busqueda_por_doi = forms.CharField(max_length  = 100)

class BusquedaRevistaForm(forms.Form):

	busqueda_por_revista = forms.CharField(max_length  = 50)

class BusquedaPalabrasClaveForm(forms.Form):

	busqueda_por_palabras_clave = forms.CharField(max_length  = 100)