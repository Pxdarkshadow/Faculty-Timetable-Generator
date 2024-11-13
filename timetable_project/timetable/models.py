from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Teacher(models.Model):
    DEPARTMENT_CHOICES = [
        ('CMPN', 'Computer Engineering'),
        ('EXTC', 'Electronics & Telecommunication'),
        ('IT', 'Information Technology'),
        ('MECH', 'Mechanical Engineering'),
        ('ELEC', 'Electrical Engineering'),
    ]
    
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)
    
    def __str__(self):
        return f"{self.name} - {self.get_department_display()}"

class Subject(models.Model):
    DEPARTMENT_CHOICES = [
        ('CMPN', 'Computer Engineering'),
        ('EXTC', 'Electronics & Telecommunication'),
        ('IT', 'Information Technology'),
        ('MECH', 'Mechanical Engineering'),
        ('ELEC', 'Electrical Engineering'),
    ]
    
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)
    
    def __str__(self):
        return f"{self.name} - {self.get_department_display()}"

class TimeSlot(models.Model):
    CLASS_TYPES = [
        ('LECTURE', 'Lecture'),
        ('PRACTICAL', 'Practical'),
    ]
    
    TIME_SLOTS = [
        ('09:00-10:00', '09:00-10:00'),
        ('10:15-11:15', '10:15-11:15'),
        ('11:15-12:15', '11:15-12:15'),
        ('13:00-14:00', '13:00-14:00'),
        ('14:00-15:00', '14:00-15:00'),
        ('15:00-16:00', '15:00-16:00'),
        ('16:00-17:00', '16:00-17:00'),
    ]
    
    DAYS = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
    ]
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAYS)
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    class_type = models.CharField(max_length=10, choices=CLASS_TYPES)
    
    class Meta:
        unique_together = ['teacher', 'day', 'time_slot']
    
    def clean(self):
        conflicts = TimeSlot.objects.filter(
            teacher=self.teacher,
            day=self.day,
            time_slot=self.time_slot
        ).exclude(pk=self.pk)
        
        if conflicts.exists():
            raise ValidationError(_('This time slot is already occupied for this teacher.'))
