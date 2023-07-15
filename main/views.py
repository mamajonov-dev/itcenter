from datetime import date, datetime

from django.db.models import Q, Sum
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View, CreateView

from .models import Pupil, Teacher, Subject, Group, Payment
from .forms import PupilForm, TeacherForm, GroupForm, SubjectForm


@login_required(login_url="login")
def index(request):
    paid_pupils_count = [pupil for pupil in Pupil.objects.all() if pupil.is_fully_paid]
    total_payed = Payment.objects.filter(month=str(datetime.now())[:7]).aggregate(Sum('amount'))['amount__sum']
    if not total_payed:
        total_payed = 0
    total_payment = Pupil.objects.aggregate(Sum('group__price'))['group__price__sum']

    context = {
        "main_top_text": "Umumiy statistika",
        "dashboard": {
            "teachers": {
                "new": Teacher.objects.filter(created__gte=date.today()).count(),
                "all": Teacher.objects.all().count()
            },
            "pupils": {
                "new": Pupil.objects.filter(created__gte=date.today()).count(),
                "all": Pupil.objects.all().count()
            },
            "subjects": {
                "new": Subject.objects.filter(created__gte=date.today()).count(),
                "all": Subject.objects.all().count()
            },
            "groups": {
                "new": Group.objects.filter(created__gte=date.today()).count(),
                "all": Group.objects.all().count()
            },
        },
        "total_payed": total_payed if total_payed else 0,
        "total_payment": total_payment if total_payment else 0,
        "total_payed_in_percent": round((total_payed / total_payment), 2) * 100 if total_payment else 0,
        "paid_pupils_count": len(paid_pupils_count),
        "unpaid_pupils_count": Pupil.objects.all().count() - len(paid_pupils_count),
    }
    return render(request, "main/index.html", context)


@login_required(login_url='login')
def paid_pupils(request):
    query = ""
    if request.GET.get('pupil'):
        query = request.GET.get('pupil')

    pupils = Pupil.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(fullname__icontains=query) |
        Q(group__teacher__fullname__icontains=query) |
        Q(group__name__icontains=query)
    ).distinct()
    pupils = [pupil for pupil in pupils if pupil.is_fully_paid]
    context = {
        "pupils": pupils,
        "main_top_text": "To'liq to'lov qilganlar",
        "search_query": query,
        "current_date": str(date.today())[:-3],
    }
    return render(request, "main/pupils_list.html", context)


@login_required(login_url='login')
def unpaid_pupils(request):
    query = ""
    if request.GET.get('pupil'):
        query = request.GET.get('pupil')

    pupils = Pupil.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(fullname__icontains=query) |
        Q(group__teacher__fullname__icontains=query) |
        Q(group__name__icontains=query)
    ).distinct()
    pupils = [pupil for pupil in pupils if not pupil.is_fully_paid]
    context = {
        "pupils": pupils,
        "main_top_text": "Qisman yoki umuman to'lov qilmaganlar",
        "search_query": query,
        "current_date": str(date.today())[:-3],
    }
    return render(request, "main/pupils_list.html", context)


# === Detail Start ===

@login_required(login_url='login')
def subject_detail(request, pk):
    query, subject = "", Subject.objects.get(id=pk)
    if request.GET.get('group'):
        query = request.GET.get('group')

    groups = Group.objects.filter(
        Q(name__icontains=query) |
        Q(teacher__fullname__icontains=query) |
        Q(subject__name__icontains=query)
    ).distinct().filter(subject_id=pk)

    if not request.user.is_superuser:
        groups = groups.filter(teacher__user=request.user)

    context = {
        "main_top_text": f"{subject.name} fani",
        "groups": groups,
        "search_query": query,
    }
    return render(request, "main/groups_list.html", context)


@login_required(login_url='login')
def group_detail(request, pk):
    query, group = "", Group.objects.get(id=pk)
    if request.GET.get('pupil'):
        query = request.GET.get('pupil')

    pupils = Pupil.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(fullname__icontains=query) |
        Q(group__teacher__fullname__icontains=query) |
        Q(group__name__icontains=query),
    ).distinct().filter(group_id=pk)

    if not request.user.is_superuser:
        pupils = pupils.filter(group__teacher__user=request.user)

    context = {
        "main_top_text": f"{group.name} guruhi",
        "pupils": pupils,
        "search_query": query,
        "current_date": str(date.today())[:-3],
    }
    return render(request, "main/pupils_list.html", context)


# === Detail End ===
# === Create Start ===
@login_required(login_url="login")
def add_pupil(request):
    if request.method == 'POST':
        try:
            pupil = Pupil.objects.get(first_name=request.POST.get('first_name'),
                                      last_name=request.POST.get('last_name'),
                                      group=request.POST.get('group'))
        except:
            pupil = None
        if pupil:
            messages.error(request, "Bunday o'quvchi bu bu guruhda allaqachon mavjud")
            return redirect("add_pupil")

        form = PupilForm(request.POST)
        if form.is_valid():
            pupil = form.save()
            pupil.fullname = f"{request.POST.get('first_name')} {request.POST.get('last_name')}"
            pupil.save()
            messages.success(request, "O'quvchi guruhga muvaffaqiyatli qo'shildi")
            return redirect("home")

    form = PupilForm()
    context = {
        "main_top_text": "Yangi o'quvchi qo'shish",
        "form": form,
        "btn_color": "success",
        "btn_text": "O'quvchini qo'shish",
    }
    return render(request, "main/crud_form.html", context)


@login_required(login_url="login")
def add_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            teacher.fullname = f"{request.POST.get('first_name')} {request.POST.get('last_name')}".title()
            teacher.save()
            return redirect("home")
        else:
            messages.error(request, "O'qituvchi qo'shishda xatolik yuz berdi")
            return redirect('add_teacher')

    form = TeacherForm()
    context = {
        "main_top_text": "Yangi o'quvchi qo'shish",
        "form": form,
        "btn_color": "info",
        "btn_text": "O'qituvchini qo'shish",
    }
    return render(request, "main/crud_form.html", context)


@login_required(login_url="login")
def add_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            messages.error(request, "Guruh qo'shishda xatolik yuz berdi")
            return redirect("add_group")

    form = GroupForm()
    context = {
        "main_top_text": "Yangi guruh qo'shish",
        "form": form,
        "btn_color": "warning",
        "btn_text": "Guruhni qo'shish",
    }
    return render(request, "main/crud_form.html", context)


@login_required(login_url='login')
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            messages.error(request, "Fan qo'shishda xatolik yuz berdi")
            return redirect("add_subject")

    form = SubjectForm()
    context = {
        "main_top_text": "Yangi fan qo'shish",
        "form": form,
        "btn_color": "primary",
        "btn_text": "Fanni qo'shish",
    }
    return render(request, "main/crud_form.html", context)


# === Create End ===
# === List Start ===

@login_required(login_url='login')
def pupils_list(request):
    query = ""
    if request.GET.get('pupil'):
        query = request.GET.get('pupil')

    pupils = Pupil.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(fullname__icontains=query) |
        Q(group__teacher__fullname__icontains=query) |
        Q(group__name__icontains=query)
    ).distinct()

    if not request.user.is_superuser:
        pupils = pupils.filter(group__teacher__user=request.user)

    context = {
        "main_top_text": "Barcha o'quvchilar",
        "pupils": pupils,
        "search_query": query,
        "current_date": str(date.today())[:-3],
    }
    return render(request, "main/pupils_list.html", context)


@login_required(login_url='login')
def teachers_list(request):
    query = ""
    if request.GET.get('teacher'):
        query = request.GET.get('teacher')

    teachers = Teacher.objects.filter(
        Q(fullname__icontains=query)
    ).distinct()
    context = {
        "main_top_text": "Barcha o'qituvchilar",
        "teachers": teachers,
        "search_query": query,
    }
    return render(request, "main/teachers_list.html", context)


@login_required(login_url='login')
def groups_list(request):
    query = ""
    if request.GET.get('group'):
        query = request.GET.get('group')

    groups = Group.objects.filter(
        Q(name__icontains=query) |
        Q(teacher__fullname__icontains=query) |
        Q(subject__name__icontains=query)
    ).distinct()

    if not request.user.is_superuser:
        groups = groups.filter(teacher__user=request.user)

    context = {
        "main_top_text": "Barcha guruhlar",
        "groups": groups,
        "search_query": query,
    }
    return render(request, "main/groups_list.html", context)


@login_required(login_url='login')
def subjects_list(request):
    query = ""
    if request.GET.get('subject'):
        query = request.GET.get('subject')

    subjects = Subject.objects.filter(
        Q(name__icontains=query)
    ).distinct()
    context = {
        "main_top_text": "Barcha fanlar",
        "subjects": subjects,
        "search_query": query,
    }
    return render(request, "main/subjects_list.html", context)


# === List End ===
# === Update Start ===
@login_required(login_url='login')
def update_pupil(request, pk):
    if request.user.is_superuser:
        pupil = Pupil.objects.get(id=pk)
    else:
        pupil = Pupil.objects.get(id=pk, group__teacher__user=request.user)

    if request.method == "POST":
        form = PupilForm(request.POST, instance=pupil)
        if form.is_valid():
            form = form.save(commit=False)
            form.fullname = f"{request.POST.get('first_name')} {request.POST.get('last_name')}"
            form.save()
            messages.success(request, "Muvaffaqiyatli o'zgartirildi")
            return redirect("pupils_list")
        else:
            messages.error(request, "Forma noto'g'ri to'ldirilgan")
            return redirect("update_pupil", pk=pk)

    form = PupilForm(instance=pupil)
    context = {
        "main_top_text": "O'quvchi ma'lumotlarini o'zgartirish",
        "form": form,
        "btn_color": "success",
        "btn_text": "Ma'lumotlarni o'zgartirish",
    }
    return render(request, "main/crud_form.html", context)


@login_required(login_url='login')
def update_teacher(request, pk):
    # identify a teacher that is going to be updated
    teacher = Teacher.objects.get(id=pk)

    # Redirecting with another uuid, if teacher is going to change another teacher's credentials
    if teacher.user != request.user and not request.user.is_superuser:
        return redirect('update_teacher', pk=request.user.teacher.id)

    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            teacher = form.save()
            teacher.fullname = f"{request.POST.get('first_name')} {request.POST.get('last_name')}"
            teacher.save()
            messages.success(request, "Muvaffaqiyatli o'zgartirildi")
            return redirect("teachers_list")
        else:
            messages.error(request, "Forma noto'g'ri to'ldirilgan")
            return redirect("update_teacher", pk=pk)

    form = TeacherForm(instance=teacher)
    context = {
        "main_top_text": "O'qituvchi ma'lumotlarini o'zgartirish",
        "form": form,
        "btn_color": "info",
        "btn_text": "Ma'lumotlarni o'zgartirish",
    }
    return render(request, "main/crud_form.html", context)


@login_required(login_url='login')
def update_subject(request, pk):
    subject = Subject.objects.get(id=pk)

    if not request.user.is_superuser:
        return redirect('subjects_list')

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Muvaffaqiyatli o'zgartirildi")
            return redirect("subjects_list")
        else:
            messages.error(request, "Forma noto'g'ri to'ldirilgan")
            return redirect("update_subject")

    form = SubjectForm(instance=subject)
    context = {
        "main_top_text": "Fan ma'lumotlarini o'zgartirish",
        "form": form,
        "btn_color": "primary",
        "btn_text": "Ma'lumotlarni o'zgartirish",
    }
    return render(request, "main/crud_form.html", context)


@login_required(login_url='login')
def update_group(request, pk):
    group = Group.objects.get(id=pk)

    if not request.user.is_superuser:
        return redirect('groups_list')

    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Muvaffaqiyatli o'zgartirildi")
            return redirect("groups_list")
        else:
            messages.error(request, "Forma noto'g'ri to'ldirilgan")
            return redirect("update_group", pk=pk)

    form = GroupForm(instance=group)
    context = {
        "main_top_text": "Guruh ma'lumotlarini o'zgartirish",
        "form": form,
        "btn_color": "warning",
        "btn_text": "Ma'lumotlarni o'zgartirish",
    }
    return render(request, "main/crud_form.html", context)


# === Update End ===
# === Payment Start ===


@login_required(login_url='login')
def create_payment(request, pk, group_id):
    if request.user.is_superuser:
        pupil, group = Pupil.objects.get(id=pk), Group.objects.get(id=group_id)
    else:
        pupil, group = Pupil.objects.get(id=pk, group__teacher__user=request.user), Group.objects.get(id=group_id)
    try:
        payment = payment = Payment.objects.get(
            month=str(date.today())[:-3],
            pupil=pupil,
            group=group
        )
    except:
        payment = None

    if request.method == 'POST':
        try:
            payment = Payment.objects.get(
                month=request.POST.get('month'),
                pupil=pupil,
                group=group
            )
        except:
            payment = None
        if not payment:
            payment = Payment.objects.create(
                owner=request.user,
                month=request.POST.get('month'),
                pupil=pupil,
                group=group,
                amount=int(request.POST.get('amount')),
                note=request.POST.get('note')
            )
            messages.success(request, 'Muvaffaqiyatli to\'landi')
        else:
            payment.amount = int(request.POST.get('amount'))
        payment.save()
        return redirect('pupils_list')

    context = {
        "pupil": pupil,
        "group": group,
        "pupils": Pupil.objects.all(),
        "current_date": str(date.today())[:-3],
        "amount": payment.amount if payment else 0,
        "max_amount": group.price,
        "main_top_text": "To'lov sahifasi"
    }
    return render(request, "main/payment.html", context)

# === Update End ===
