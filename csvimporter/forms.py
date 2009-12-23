import csv

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.conf import settings

from csvimporter.models import CSV

class CSVForm(forms.ModelForm):
    class Meta:
        model = CSV
    exclude_types = getattr(settings, 'CSVIMPORTER_EXCLUDE', [])
    # TODO: this could be so much nicer.
    content_types = ContentType.objects.all()
    for t in exclude_types:
        if '.' in t:
            content_types = content_types.exclude(app_label__iexact=t.split('.')[0], model__iexact=t.split('.')[1].lower())
        else:
            content_types = content_types.exclude(app_label__iexact=t)
    content_type = forms.ModelChoiceField(queryset=content_types)
    
key_to_field_map = getattr(settings, 'CSVIMPORTER_KEY_TO_FIELD_MAP', lambda k: k.replace(' ','_').lower())
class CSVAssociateForm(forms.Form):
    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        self.reader = csv.DictReader(instance.csv_file)
        self.reader.next()
        self.klass = self.instance.content_type.model_class()
        choices = [(None,'---- (None)')] + [(f.name, f.name) for f in self.klass._meta.fields]
        # self.base_fields gets copied over to create self.fields in __init__
        self.base_fields = {}
        for field_name in self.reader.fieldnames:
            self.base_fields[field_name] = forms.ChoiceField(choices=choices, required=False)
            if key_to_field_map(field_name) in [f.name for f in self.klass._meta.fields]:
                self.base_fields[field_name].initial = key_to_field_map(field_name)
        super(CSVAssociateForm, self).__init__(*args, **kwargs)
        
    def save(self, request):
        # these are out here because we only need to retreive them from settings the once.
        transforms = getattr(settings, 'CSVIMPORTER_DATA_TRANSFORMS', {})
        for row in self.reader:
            data = {}
            for field_name in self.reader.fieldnames:
                data[self.cleaned_data[field_name]] = row[field_name]
            transform_key = '%s.%s' % (self.instance.content_type.app_label, self.instance.content_type.model)
            data = transforms.get(transform_key, lambda r, d: d)(request, data)
            new_obj = self.klass()
            for key in data.keys():
                setattr(new_obj, key, data[key])
            new_obj.save()
        self.instance.delete()