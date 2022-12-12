from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from .utils import context_provider, upload_file_to_path

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = {}
        context["data"] = context_provider
        return context


class CsvFileView(View):
    def get(self, request, id=1):
        context = {}
        context["name"] = context_provider[id][2]
        context["info"] = context_provider[id][3]
        return render(request, "upload_template.html", context)

    def post(self, request, id=1):
        path = upload_file_to_path(request.FILES["file"])
        data = context_provider[id]
        output, time_stamp , memory = data[0](path, data[1])
        context = {}
        context["name"] = context_provider[id][2]
        context["info"] = context_provider[id][3]
        context["response"] = True
        context["rows"] = output[:50]
        context["time"] = time_stamp
        context["memory"] = memory
        return render(request, "upload_template.html", context)
