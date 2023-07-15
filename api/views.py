from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import GroupSerializer, SubjectSerializer

from main.models import Group, Pupil, Subject, Teacher


def delete(item):
    deleted = 'false'
    try:
        item.delete()
        deleted = 'true'
    except:
        pass

    return deleted


@api_view(['GET'])
def group_subject_delete(request):
    model_name = request.GET.get('model')
    pk = request.GET.get('pk')

    if model_name == 'group':
        item = Group.objects.get(id=pk)
    if model_name == 'subject':
        item = Subject.objects.get(id=pk)

    if request.GET.get('confirm'):
        return Response({
            'deleted': delete(item),
            'pk': pk,
        })
    else:
        if model_name == 'group':
            serialized_item = GroupSerializer(item, many=False).data
            serialized_item[
                'confirmationText'] = f"{serialized_item.get('name')} guruhini o'chirishga ishinchingiz komilmi ? " \
                                      f"Agar davom etsangiz, guruh va bu guruhda ro'yxatda olingan barcha o'quvchilar " \
                                      f"butkul o'chib ketadi"

        elif model_name == 'subject':
            serialized_item = SubjectSerializer(item, many=False).data
            serialized_item[
                'confirmationText'] = f"{serialized_item.get('name')} fanini o'chirishga ishinchingiz komilmi ? " \
                                      f"Agar davom etsangiz, fan va bu fan bilan bog'liq barcha guruhlar butkul " \
                                      f"o'chib ketadi"

        return Response(serialized_item)
