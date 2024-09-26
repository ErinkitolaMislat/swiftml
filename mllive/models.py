from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

import os
from django.core.exceptions import ValidationError
User = get_user_model()

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.pkl', '.joblib']
    if ext.lower() not in valid_extensions:
        raise ValidationError(
            'Unsupported file extension. Allowed extensions are: .pkl, .joblib')

class SklearnModel(models.Model):
    model_name = models.CharField(max_length=100, unique=True)
    model_file = models.FileField(upload_to='models/', validators=[validate_file_extension])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='models')

    def __str__(self):
        return self.model_name
    
class SklearnModelInput(models.Model):
    model = models.ForeignKey(SklearnModel, on_delete=models.CASCADE, related_name='inputs')
    input_name = models.CharField(max_length=100, )

    def __str__(self):
        return self.input_name
    
class SklearnModelOutput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outputs')
    model = models.ForeignKey(SklearnModel, on_delete=models.CASCADE, related_name='outputs')
    output_value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.output_value