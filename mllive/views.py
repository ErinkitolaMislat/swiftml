from django.contrib.auth import get_user_model
import pandas as pd
import joblib

from .models import SklearnModel, SklearnModelInput
from .forms import SklearnModelForm, SklearnModelInputForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.
User = get_user_model()

@login_required
def index(request):
    return render(request, 'index.html')


# views.py


@login_required
def upload_model(request):
    if request.method == 'POST':
        print(request.user.id)
        form = SklearnModelForm(request.POST, request.FILES)
        if form.is_valid():
            sklearn_model = form.save(commit=False)
            sklearn_model.user = User.objects.get(id=request.user.id)
            print(request.user)
            sklearn_model.save()
            input_names = request.POST.getlist('input_names')
            for input_name in input_names:
                SklearnModelInput.objects.create(
                    model=sklearn_model, input_name=input_name)
            return redirect('model_list')
        else:
            return render(request, 'upload_model.html', {'form': form})
    else:
        form = SklearnModelForm()
    return render(request, 'upload_model.html', {'form': form})


@login_required
def add_input_field(request):
    new_index = request.GET.get('index', 0)
    html = render_to_string('input_field.html', {'index': new_index})
    return HttpResponse(html)

@login_required
def model_list(request):
    models = SklearnModel.objects.filter(user=request.user)
    return render(request, 'model_list.html', {'models': models})


def predict(request, model_id):
    model = get_object_or_404(SklearnModel, id=model_id)
    if request.method == 'POST':
        input_data = {input.input_name: float(
            request.POST[input.input_name]) for input in model.inputs.all()} #type: ignore
        input_df = pd.DataFrame([input_data])
        model_file = model.model_file.path #type: ignore
        try:
            loaded_model = joblib.load(model_file)
            prediction = loaded_model.predict(input_df)
        except Exception as e:
            return render(request, 'predict.html', {'model': model, 'error': str(e)})
        return render(request, 'predict.html', {'model': model, 'prediction': prediction[0]})
    return render(request, 'predict.html', {'model': model})


def delete_model(request, model_id):
    model = get_object_or_404(SklearnModel, id=model_id, user = request.user)
    model.delete()
    return redirect('model_list')


def bad_request(request, exception):
    return render(request, '400.html', status=400)


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)
