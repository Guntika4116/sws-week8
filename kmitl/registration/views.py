from django.shortcuts import render, redirect
from registration.models import Student, Professor, Course, Faculty, StudentProfile, Section

from django.db.models import Value, Q, Count
from django.db.models.functions import Concat



# Create your views here.
# def student_list(request):
#     student_list = Student.objects.all()
    
#     return render(request, "index.html", context={
#         "total": student_list.count(),
#         "student_list": student_list
#     })
from django.db.models import Value
from django.db.models.functions import Concat

def student_list(request):
    search = request.GET.get("search", "").strip()
    filter_type = request.GET.get("filter", "")

    students = Student.objects.all()

    if search:
        if filter_type == "faculty":
            # faculty อยู่ในตาราง Faculty
            students = students.filter(faculty__name__icontains=search)
        elif filter_type == "email":
            # email อยู่ใน studentprofile
            students = students.filter(studentprofile__email__icontains=search)
        else:  # default = full name
            students = students.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(full_name__icontains=search)

    return render(request, "index.html", {
        "total": students.count(),
        "student_list": students,
        "search": search,
        "filter": filter_type,
    })


# def professor_list(request):
#     professor_list = Professor.objects.all()
#     return render(request, "professor.html", context={
#         "total": professor_list.count(),
#         "professor_list": professor_list
#     })
def professor_list(request):
    search = request.GET.get("search", "").strip()
    filter_type = request.GET.get("filter", "")
    professor_list = Professor.objects.all()

    if search:
        if filter_type == "faculty":
            professor_list = Professor.objects.filter(faculty__name__icontains=search)
        else:
            professor_list = Professor.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(
                Q(full_name__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )

    return render(request, 'professor.html', context={
        'total': professor_list.count(),
        'professor_list': professor_list,
        'search': search,
        'filter': filter_type,
    })

# def course_list(request):
#     course_list = Course.objects.all()
#     return render(request, "course.html", context={
#         "total": course_list.count(),
#         "course_list": course_list
        
#     })
def course_list(request):
    search = request.GET.get("search", "").strip()
    courses = Course.objects.all()

    if search:
        courses = courses.filter(course_name__icontains=search)

    return render(request, "course.html", {
        "total": courses.count(),
        "course_list": courses,
        "search": search,
    })



def faculty_list(request):
    faculty_list = Faculty.objects.annotate(
        professor_num=Count("professors", distinct=True),
        student_num=Count("students", distinct=True)
    ).all()

    search = request.GET.get("search", "").strip()
    if search:
        faculty_list = faculty_list.filter(name__icontains=search)

    return render(request, "faculty.html", context={
        "total": faculty_list.count(),
        "faculty_list": faculty_list,
        "search": search,
    })




def create_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        faculty_id = request.POST.get('faculty')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        address = request.POST.get('address')
        section_ids = request.POST.getlist('section_ids')  # multiple select

        # สร้าง Student
        student = Student.objects.create(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            faculty=Faculty.objects.get(id=faculty_id)
        )

        # สร้าง StudentProfile
        StudentProfile.objects.create(
            student=student,
            email=email,
            phone_number=phone,
            address=address
        )

        # ผูก sections ถ้ามีเลือก
        if section_ids:
            student.enrolled_sections.set(section_ids)

        return redirect('student_list')  # <-- เด้งกลับหน้ารายชื่อนักเรียน

    faculties = Faculty.objects.all()
    sections = Section.objects.select_related('course').all()
    return render(request, 'create_student.html', {
        'faculties': faculties,
        'sections': sections
    })