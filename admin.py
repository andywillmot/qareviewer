from django.contrib import admin
from qareviewer.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ActivityResource (resources.ModelResource):
    class Meta:
        model = Activity

class ActivityAdmin(ImportExportModelAdmin):
    resource_class = ActivityResource

class AcceptanceCriteriaResource(resources.ModelResource):
    class Meta:
        model = AcceptanceCriteria

class AcceptanceCriteriaAdmin(ImportExportModelAdmin):
    resource_class = AcceptanceCriteriaResource

class ThemeResource (resources.ModelResource):
    class Meta:
        model = Theme

class ThemeAdmin(ImportExportModelAdmin):
    resource_class = ThemeResource

class TemplateDeliverableResource (resources.ModelResource):
    class Meta:
        model = TemplateDeliverable

class TemplateDeliverableAdmin(ImportExportModelAdmin):
    resource_class = TemplateDeliverableResource

class TemplateDeliverableSectionResource (resources.ModelResource):
    class Meta:
        model = TemplateDeliverableSection

class TemplateDeliverableSectionAdmin(ImportExportModelAdmin):
    resource_class = TemplateDeliverableSectionResource



admin.site.register(Activity,ActivityAdmin)
admin.site.register(Theme,ThemeAdmin)
admin.site.register(TemplateDeliverable,TemplateDeliverableAdmin)
admin.site.register(TemplateDeliverableSection,TemplateDeliverableSectionAdmin)
admin.site.register(AcceptanceCriteria,AcceptanceCriteriaAdmin)
