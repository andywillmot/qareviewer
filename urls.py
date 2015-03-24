from django.conf.urls import patterns, url, include
from qareviewer.views import *
from .tables import *

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    url(r'^$', DeliverableList.as_view()),
    url(r'^deliverables/$', DeliverableList.as_view(),name='deliverable-list'),
    url(r'^deliverable/create$', DeliverableCreate.as_view(),name='deliverable-create'),
    url(r'^deliverable/(?P<pk>\d+)/$', DeliverableUpdate.as_view(),name='deliverable-detail'),
    url(r'^reviewiterations/$', ReviewIterationList.as_view(),name='reviewiteration-list'),
    url(r'^reviewiterations/\?deliverable__id=(?P<pk>\d+)$', ReviewIterationList.as_view(),name='reviewiteration-list-filter'),
    url(r'^reviewiteration/create$', ReviewIterationCreate.as_view(),name='reviewiteration-create'),
    url(r'^reviewiterations/create\?deliverable__id=(?P<pk>\d+)$', ReviewIterationCreate.as_view(),name='reviewiteration-create'),
    url(r'^reviewiteration/(?P<pk>\d+)/$', ReviewIterationUpdate.as_view(),name='reviewiteration-detail'),
    url(r'^comments/$', CommentList.as_view(),name='comment-list'),
    url(r'^comments/\?reviewiteration__id=(?P<pk>\d+)$', CommentList.as_view(),name='comment-list-filter'),
    url(r'^comment/create$', CommentCreate.as_view(),name='comment-create'),
    url(r'^comment/(?P<pk>\d+)/$', CommentUpdate.as_view(),name='comment-detail'),

    #export
    url(r'^deliverables/export$', DeliverableExport.as_view(), name='deliverable_export'),

    #import
    url(r'^deliverables/import$', DeliverableImport.as_view(), name='deliverable_import'),
    url(r'^deliverables/process_import$', DeliverableProcessImport.as_view(), name='process_import'),
)

urlpatterns += staticfiles_urlpatterns()
