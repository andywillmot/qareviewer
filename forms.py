from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

class DeliverableListFormHelper(FormHelper):
    model = Deliverable
    form_tag = True
    attrs = {"role": "form"}

class ReviewIterationListFormHelper(FormHelper):
    model = ReviewIteration
    form_tag = True
    attrs = {"role": "form"}
#    layout = Layout('pk', ButtonHolder(
#        Submit('submit', 'Filter', css_class='btn btn-default')
#    ))
    
class CommentListFormHelper(FormHelper):
    model = Comment
    form_tag = True   
    attrs = {"role": "form"}
    layout = Layout('review_iteration','template_deliverable_section', ButtonHolder(
        Submit('submit', 'Filter', css_class='btn btn-default')
    ))

    
