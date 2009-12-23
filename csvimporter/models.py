from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class CSV(models.Model):
    
    content_type = models.ForeignKey(ContentType)
    csv_file     = models.FileField(upload_to=getattr(settings, 'CSVIMPORTER_UPLOAD_TO', 'csvimporter'))
    created      = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        """
        This is a helper method, so that you can display the name of the file a user uploaded, without
        the name of the directory the file was uploaded to.
        """
        return self.csv_file.name.replace('%s/' % upload_to, '')