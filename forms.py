from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django.core.urlresolvers import reverse

class DeliverableListFormHelper(FormHelper):
    model = Deliverable
    form_tag = False

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

class DeliverableForm(forms.ModelForm):
    class Meta:
        model = Deliverable
#    def __init__(self, *args, **kwargs):
#        super(DeliverableForm, self).__init__(*args, **kwargs)
#        self.helper = DeliverableFormHelper()
#        self.helper.form_id = 'id-exampleForm'
#        self.helper.form_class = 'blueForms'
#        self.helper.form_method = 'post'
#        self.helper.form_action = reverse('qareviewer:deliverable-create')
#        self.helper.add_input(Submit('submit', 'Submit'))

class ReviewIterationForm(forms.ModelForm):
    class Meta:
        model = ReviewIteration
    def __init__(self, *args, **kwargs):
        super(ReviewIterationForm, self).__init__(*args, **kwargs)
        self.helper = ReviewIterationFormHelper()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = CommentFormHelper()
    
