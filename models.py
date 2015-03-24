from django.db import models
from import_export import resources

class Activity(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Theme(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class TemplateDeliverable(models.Model):
    activity = models.ForeignKey(Activity,null=True,blank=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.activity) + ':' + self.name

class TemplateDeliverableSection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    purpose = models.TextField( )
    template_deliverable = models.ForeignKey(TemplateDeliverable,null=True,blank=True)
    def __str__(self):
        return self.name

class AcceptanceCriteria(models.Model):
    criteria = models.CharField(max_length=1000)
    deliverable_section = models.ForeignKey(TemplateDeliverableSection)
    def __str__(self):
        return self.criteria

class Deliverable(models.Model):
    template_deliverable = models.ForeignKey(TemplateDeliverable)
    theme = models.ForeignKey(Theme)
    date_first_issued = models.DateField('Date First Issued',null=True,blank=True)
    date_signed_off = models.DateField('Date Signed Off',null=True,blank=True)
    def __str__(self):
        return self.theme.name + ' - ' + self.template_deliverable.name

class ReviewIteration(models.Model):
    deliverable = models.ForeignKey(Deliverable)
    version = models.CharField(max_length=30,null=True,blank=True)
    iteration_number = models.BigIntegerField('Iteration No.')
    publisher = models.CharField(max_length=40,null=True,blank=True)
    issued_date = models.DateTimeField('Date Issued',null=True,blank=True)
    reviewer = models.CharField(max_length=40,null=True,blank=True)
    review_date = models.DateTimeField('Date Reviewed',null=True,blank=True)
    def __str__(self):
        return str(self.deliverable) + ':' + self.version + ' iter. ' + str(self.iteration_number)

class Comment(models.Model):
    SIGNOFFCHOICES = (
        ('Matr','Material'),
        ('Cond','Conditional'),
        ('Good','Good to have'),
        ('Comp','Compliant'),
    )
    review_iteration = models.ForeignKey(ReviewIteration,related_name='review_iteration')
    iteration_comment_closed = models.ForeignKey(ReviewIteration,related_name='iteration_comment_closed',null=True,blank=True)
    template_deliverable_section = models.ForeignKey(TemplateDeliverableSection,null=True,blank=True)
    acceptance_critieria = models.ForeignKey(AcceptanceCriteria, null=True,blank=True)
    comment_location = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField()
    sign_off_type = models.CharField(max_length=15,choices=SIGNOFFCHOICES)
    actions_to_close = models.TextField(null=True,blank=True)
    action_comments = models.TextField(null=True,blank=True)
    date_closed = models.DateTimeField('Date Comment Closed',null=True,blank=True)
    def __str__(self):
        return self.review_iteration + ':' + self.pk


class DeliverableResource(resources.ModelResource):
    class Meta:
        model = Deliverable

class ReviewIterationResource(resources.ModelResource):
    class Meta:
        model = ReviewIteration

class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment


