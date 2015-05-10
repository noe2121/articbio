from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'articbio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'appcore.views.home', name='home'),
	url(r'^subir_articulo/', 'appcore.views.subir_articulo', name='subir_articulo'),
	url(r'^capturar_articulo/', 'appcore.views.capturar_articulo', name='capturar_articulo'),
	url(r'^busquedas/', 'appcore.views.busquedas', name='busquedas'),
	url(r'^mostrar_todos_eliminar/', 'appcore.views.mostrar_todos_eliminar', name='mostrar_todos_eliminar'),
	url(r'^mostrar_articulo_por_id/(\d+)/', 'appcore.views.mostrar_articulo_por_id', name='mostrar_articulo_por_id'),
	url(r'^eliminar_por_id/(\d+)/', 'appcore.views.eliminar_por_id', name='eliminar_por_id'),
	
    url(r'^admin/', include(admin.site.urls)),
)
