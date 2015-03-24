import django_tables2 as dt2
from django_tables2.utils import A  # alias for Accessor
from .models import *
from django.core.urlresolvers import reverse

class DeliverableTable(dt2.Table):
    class Meta:
        model = Deliverable
        attrs = {"class": "table table-striped table-hover table-condensed"}
        per_page = 30

    id = dt2.LinkColumn('qareviewer:deliverable-detail',args=[A('pk')])
    template_deliverable = dt2.LinkColumn('qareviewer:reviewiteration-list-filter',args=[A('pk')])
    review_iterations = dt2.LinkColumn('qareviewer:reviewiteration-list-filter',args=[A('pk')],accessor='ReviewIterations.objects.filter(deliverable=pk)')
    #,orderable=False,empty_values=())

#    def render_action(self):
#        theid = A('self.pk')
#        url = '<a href="%s?deliverable__id=' + theid + '"> Go...</a'
#        return  url % reverse('qareviewer:reviewiteration-list')

class ReviewIterationTable(dt2.Table):
    class Meta:
        model = ReviewIteration
        attrs = {"class": "table table-striped table-hover table-condensed"}
        per_page = 30

    id = dt2.LinkColumn('qareviewer:reviewiteration-detail',args=[A('pk')])
    deliverable = dt2.LinkColumn('qareviewer:comment-list-filter',args=[A('pk')])  

class CommentTable(dt2.Table):
    class Meta:
        model = Comment
        attrs = {"class": "table table-striped table-hover table-condensed"}
        per_page = 30

    id = dt2.LinkColumn('qareviewer:comment-detail',args=[A('pk')])
