from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Teacher, Subject, TimeSlot
from .forms import TeacherForm, SubjectForm, TimeSlotForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def home(request):
    return render(request, 'timetable/home.html')

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully!')
            return redirect('home')  # Changed from teacher_list to home
    else:
        form = TeacherForm()
    return render(request, 'timetable/add_teacher.html', {'form': form})

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully!')
            return redirect('home')  # Changed from subject_list to home
    else:
        form = SubjectForm()
    return render(request, 'timetable/add_subject.html', {'form': form})

def teacher_list(request):
    teachers = Teacher.objects.all().order_by('department', 'name')
    return render(request, 'timetable/teacher_list.html', {'teachers': teachers})

def subject_list(request):
    subjects = Subject.objects.all().order_by('department', 'name')
    return render(request, 'timetable/subject_list.html', {'subjects': subjects})

def add_timeslot(request):
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            try:
                time_slot = form.save(commit=False)
                
                conflicts = TimeSlot.objects.filter(
                    teacher=time_slot.teacher,
                    day=time_slot.day,
                    time_slot=time_slot.time_slot
                ).exclude(pk=time_slot.pk)
                
                if time_slot.class_type == 'PRACTICAL':

                    start_time, end_time = map(lambda x: x.strip(), time_slot.time_slot.split('-'))
                    

                    conflicts |= TimeSlot.objects.filter(
                        teacher=time_slot.teacher,
                        day=time_slot.day,
                        time_slot__range=(start_time, end_time)
                    ).exclude(pk=time_slot.pk)
                
                if conflicts.exists():
                    raise ValidationError(('This time slot is already occupied for this teacher.'))
                
                time_slot.save()
                messages.success(request, 'Time slot added successfully!')
                return redirect('timetable_view')
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = TimeSlotForm()
    return render(request, 'timetable/add_timeslot.html', {'form': form})

def edit_timeslot(request, pk):
    timeslot = get_object_or_404(TimeSlot, pk=pk)
    if request.method == 'POST':
        form = TimeSlotForm(request.POST, instance=timeslot)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Time slot updated successfully!')
                return redirect('timetable_view')
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = TimeSlotForm(instance=timeslot)
    return render(request, 'timetable/edit_timeslot.html', {'form': form})

def delete_timeslot(request, pk):
    timeslot = get_object_or_404(TimeSlot, pk=pk)
    timeslot.delete()
    messages.success(request, 'Time slot deleted successfully!')
    return redirect('timetable_view')

def timetable_view(request):
    teachers = Teacher.objects.all().order_by('department', 'name')
    selected_teacher = request.GET.get('teacher')
    time_slots = dict(TimeSlot.TIME_SLOTS)
    days = dict(TimeSlot.DAYS)
    
    if selected_teacher:
        teacher = Teacher.objects.get(id=selected_teacher)
        timeslots = TimeSlot.objects.filter(teacher=teacher).order_by('day', 'time_slot')
    else:
        timeslots = []
        teacher = None
    
    return render(request, 'timetable/timetable_view.html', {
        'teachers': teachers,
        'selected_teacher': teacher,
        'timeslots': timeslots,
        'time_slots': TimeSlot.TIME_SLOTS,
        'days': TimeSlot.DAYS
    })

def generate_pdf(request, teacher_id):
    # Get the teacher and their timeslots
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    timeslots = TimeSlot.objects.filter(teacher=teacher).order_by('day', 'time_slot')
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="timetable_{teacher.name}.pdf"'
    
    # Create the PDF object using reportlab
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    # Add title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Timetable for {teacher.name}")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 70, f"Department: {teacher.get_department_display()}")
    
    # Prepare data for table
    data = [['Time/Day', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]
    
    # Get all time slots
    all_time_slots = [slot[0] for slot in TimeSlot.TIME_SLOTS]
    all_days = [day[0] for day in TimeSlot.DAYS]
    
    # Create dictionary for quick lookup of timeslots
    slot_dict = {}
    for slot in timeslots:
        slot_dict[(slot.day, slot.time_slot)] = slot
    
    # Fill in the timetable data
    for time in all_time_slots:
        row = [time]  # First column is the time
        for day in all_days:
            slot = slot_dict.get((day, time))
            if slot:
                cell_text = f"{slot.subject.name}\n({slot.get_class_type_display()})"
            else:
                cell_text = ""
            row.append(cell_text)
        data.append(row)
    
    # Create table
    table = Table(data, colWidths=[80] + [90]*5, rowHeights=[30] + [50]*len(all_time_slots))
    
    # Add style to table
    style = TableStyle([
        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        
        # Time column
        ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        
        # Rest of the cells
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 1), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    table.setStyle(style)
    
    # Draw the table
    table.wrapOn(p, width - 100, height)
    table.drawOn(p, 50, height - 500)  # Adjust the last number to move table up or down
    
    # Add footer with date
    from datetime import datetime
    p.setFont("Helvetica", 8)
    p.drawString(50, 30, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save the PDF
    p.showPage()
    p.save()
    
    return response
