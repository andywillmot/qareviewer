from django.shortcuts import render
from django.views import generic
from qareviewer.models import *
from qareviewer.tables import *
from qareviewer.filters import *
from qareviewer.forms import *
from django_tables2 import SingleTableView
from qareviewer.utils import *
from import_export.formats import base_formats
from import_export.resources import modelresource_factory
from import_export.forms import ImportForm
from django.http import HttpResponse
from django.template.response import TemplateResponse

from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class DeliverableList(LoginRequiredMixin,FilteredSingleTableView):
    model = Deliverable
    table_class = DeliverableTable
    filter_class = DeliverableListFilter
#    formhelper_class = DeliverableListFormHelper

class DeliverableCreate(LoginRequiredMixin,generic.CreateView):
    model=Deliverable
    template_name = 'qareviewer/deliverable_form.html'
    form_class = DeliverableForm
    def get_success_url(self):
        return reverse('qareviewer:deliverable-list')

class DeliverableUpdate(LoginRequiredMixin,generic.UpdateView):
    model=Deliverable
    template_name = 'qareviewer/deliverable_form.html'
    form_class = DeliverableForm
    def get_success_url(self):
        return reverse('qareviewer:deliverable-list')

class ReviewIterationList(LoginRequiredMixin,FilteredSingleTableView):
    model=ReviewIteration
    table_class=ReviewIterationTable
    filter_class = ReviewIterationListFilter
#    formhelper_class = ReviewIterationListFormHelper

class ReviewIterationCreate(generic.CreateView):
    model=ReviewIteration
    template_name = 'qareviewer/reviewiteration_form.html'
    form_class = ReviewIterationForm
    def get_success_url(self):
        return reverse('qareviewer:reviewiteration-list')

class ReviewIterationUpdate(generic.UpdateView):
    model=ReviewIteration
    template_name = 'qareviewer/reviewiteration_form.html'
    form_class = ReviewIterationForm
    def get_success_url(self):
        return reverse('qareviewer:reviewiteration-list')

class CommentList(LoginRequiredMixin,FilteredSingleTableView):
    model=Comment
    table_class=CommentTable
    filter_class = CommentListFilter
#    formhelper_class = CommentListFormHelper

class CommentCreate(generic.CreateView):
    model=Comment
    template_name = 'qareviewer/comment_form.html'
    form_class = CommentForm
    def get_success_url(self):
        return reverse('qareviewer:comment-list')

class CommentUpdate(generic.UpdateView):
    model=Comment
    template_name = 'qareviewer/comment_form.html'
    form_class = CommentForm
    def get_success_url(self):
        return reverse('qareviewer:comment-list')


#import export stuff

class DeliverableExport(generic.View):

    def get(self, *args, **kwargs ):
        dataset = DeliverableResource().export()
        response = HttpResponse(dataset.csv, content_type="csv")
        response['Content-Disposition'] = 'attachment; filename=filename.csv'
        return response


class DeliverableImport(generic.View):
    model = Deliverable
    from_encoding = "utf-8"

    #: import / export formats
    DEFAULT_FORMATS = (
        base_formats.CSV,
        base_formats.XLS,
        base_formats.TSV,
        base_formats.ODS,
        base_formats.JSON,
        base_formats.YAML,
        base_formats.HTML,
    )
    formats = DEFAULT_FORMATS
    #: template for import view
    import_template_name = 'import.html'
    resource_class = None

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_import_resource_class(self):
        """
        Returns ResourceClass to use for import.
        """
        return self.get_resource_class()

    def get(self, *args, **kwargs ):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource_class()()

        context = {}

        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          self.request.POST or None,
                          self.request.FILES or None)

        if self.request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
                for chunk in import_file.chunks():
                    uploaded_file.write(chunk)

            # then read the file, using the proper format-specific mode
            with open(uploaded_file.name,
                      input_format.get_read_mode()) as uploaded_import_file:
                # warning, big files may exceed memory
                data = uploaded_import_file.read()
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
                result = resource.import_data(dataset, dry_run=True,
                                              raise_errors=False)

            context['result'] = result

            if not result.has_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': os.path.basename(uploaded_file.name),
                    'input_format': form.cleaned_data['input_format'],
                })

        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        return TemplateResponse(self.request, [self.import_template_name], context)


    def post(self, *args, **kwargs ):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource_class()()

        context = {}

        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          self.request.POST or None,
                          self.request.FILES or None)

        if self.request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
                for chunk in import_file.chunks():
                    uploaded_file.write(chunk)

            # then read the file, using the proper format-specific mode
            with open(uploaded_file.name,
                      input_format.get_read_mode()) as uploaded_import_file:
                # warning, big files may exceed memory
                data = uploaded_import_file.read()
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
                result = resource.import_data(dataset, dry_run=True,
                                              raise_errors=False)

            context['result'] = result

            if not result.has_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': os.path.basename(uploaded_file.name),
                    'input_format': form.cleaned_data['input_format'],
                })

        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        return TemplateResponse(self.request, [self.import_template_name], context)

class DeliverableProcessImport(generic.View):
    model = Deliverable
    from_encoding = "utf-8"

    #: import / export formats
    DEFAULT_FORMATS = (
        base_formats.CSV,
        base_formats.XLS,
        base_formats.TSV,
        base_formats.ODS,
        base_formats.JSON,
        base_formats.YAML,
        base_formats.HTML,
    )
    formats = DEFAULT_FORMATS
    #: template for import view
    import_template_name = 'import.html'
    resource_class = None

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_import_resource_class(self):
        """
        Returns ResourceClass to use for import.
        """
        return self.get_resource_class()

    def post(self, *args, **kwargs ):
        '''
        Perform the actual import action (after the user has confirmed he
    wishes to import)
        '''
        opts = self.model._meta
        resource = self.get_import_resource_class()()

        confirm_form = ConfirmImportForm(self.request.POST)
        if confirm_form.is_valid():
            import_formats = self.get_import_formats()
            input_format = import_formats[
                int(confirm_form.cleaned_data['input_format'])
            ]()
            import_file_name = os.path.join(
                tempfile.gettempdir(),
                confirm_form.cleaned_data['import_file_name']
            )
            import_file = open(import_file_name, input_format.get_read_mode())
            data = import_file.read()
            if not input_format.is_binary() and self.from_encoding:
                data = force_text(data, self.from_encoding)
            dataset = input_format.create_dataset(data)

            result = resource.import_data(dataset, dry_run=False,
                                 raise_errors=True)

            # Add imported objects to LogEntry
            ADDITION = 1
            CHANGE = 2
            DELETION = 3
            logentry_map = {
                RowResult.IMPORT_TYPE_NEW: ADDITION,
                RowResult.IMPORT_TYPE_UPDATE: CHANGE,
                RowResult.IMPORT_TYPE_DELETE: DELETION,
            }
            content_type_id=ContentType.objects.get_for_model(self.model).pk
            '''
            for row in result:
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=content_type_id,
                    object_id=row.object_id,
                    object_repr=row.object_repr,
                    action_flag=logentry_map[row.import_type],
                    change_message="%s through import_export" % row.import_type,
                )
            '''
            success_message = _('Import finished')
            messages.success(self.request, success_message)
            import_file.close()

            url = reverse('%s_list' % (str(opts.app_label).lower()))
            return HttpResponseRedirect(url)
