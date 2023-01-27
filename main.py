from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import View
from api.models import Course
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import OperationalError, ProgrammingError

class LearnerCourses(View):
    template = "my_courses.html"

    def get(self, request, *args, **kwargs):
        all_courses=Course.objects.all()

        page = request.GET.get('page')
        result = 60
        paginator = Paginator(all_courses, result)
        try:
            all_courses=paginator.page(page)
        except PageNotAnInteger:
            page=1
            all_courses = paginator.page(page)
        except EmptyPage:
            page=paginator.num_pages
            all_courses = paginator.page(page)
        except ProgrammingError:
            all_courses=Course.objects.all()

        leftIndex = (int(page) - 4)

        if leftIndex < 1:
            leftIndex=1

        rightIndex = (int(page) + 5)

        if rightIndex > paginator.num_pages:
            rightIndex = paginator.num_pages + 1


        custom_range= range(leftIndex, rightIndex)

        context = {
            'all_courses':all_courses,
            'paginator':paginator,
            'custom_range': custom_range,
        }
        return render(request, self.template, context)