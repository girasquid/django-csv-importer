from django.conf.urls.defaults import *

urlpatterns = patterns('csvimporter.views',
    url(r'^$', 'csv_list', name='csv-list'),
    url(r'^new/$', 'new', name='new-csv'),
    url(r'^(?P<object_id>\d+)/$', 'associate', name='associate-csv'),
)