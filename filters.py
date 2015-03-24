import django_filters as df
from .models import *

class DeliverableListFilter(df.FilterSet):
    class Meta:
        model = Deliverable
        fields = ['theme__name']

class ReviewIterationListFilter(df.FilterSet):
    class Meta:
        model = ReviewIteration
        fields = ['deliverable__id']

class CommentListFilter(df.FilterSet):
    class Meta:
        model = Comment
        fields = ['review_iteration__id']
